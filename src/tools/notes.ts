import { createSdkMcpServer, tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";
import { promises as fs } from "node:fs";
import path from "node:path";
import { randomUUID } from "node:crypto";

const STORE_PATH = path.resolve(process.cwd(), "data", "notes.json");

type Kind = "note" | "task";

interface Entry {
  id: string;
  kind: Kind;
  content: string;
  tags: string[];
  done: boolean;
  createdAt: string;
}

interface Store {
  entries: Entry[];
}

async function loadStore(): Promise<Store> {
  try {
    const raw = await fs.readFile(STORE_PATH, "utf8");
    return JSON.parse(raw) as Store;
  } catch (err: unknown) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") {
      return { entries: [] };
    }
    throw err;
  }
}

async function saveStore(store: Store): Promise<void> {
  await fs.mkdir(path.dirname(STORE_PATH), { recursive: true });
  await fs.writeFile(STORE_PATH, JSON.stringify(store, null, 2) + "\n", "utf8");
}

function formatEntry(e: Entry): string {
  const status = e.kind === "task" ? (e.done ? "[x]" : "[ ]") : "•";
  const tags = e.tags.length ? ` (${e.tags.map((t) => `#${t}`).join(" ")})` : "";
  return `${status} ${e.id.slice(0, 8)} — ${e.content}${tags}`;
}

export const notesServer = createSdkMcpServer({
  name: "notes",
  version: "0.1.0",
  tools: [
    tool(
      "add",
      "Add a note or task to the local store. Use kind='task' for todos, 'note' for free-form notes.",
      {
        kind: z.enum(["note", "task"]).describe("Type of entry"),
        content: z.string().min(1).describe("The note or task text"),
        tags: z.array(z.string()).optional().describe("Optional tags, e.g. ['work', 'urgent']"),
      },
      async (args) => {
        const store = await loadStore();
        const entry: Entry = {
          id: randomUUID(),
          kind: args.kind,
          content: args.content,
          tags: args.tags ?? [],
          done: false,
          createdAt: new Date().toISOString(),
        };
        store.entries.push(entry);
        await saveStore(store);
        return {
          content: [{ type: "text", text: `Added ${args.kind}: ${formatEntry(entry)}` }],
        };
      },
    ),

    tool(
      "list",
      "List notes and tasks. Filter by kind, tag, or completion status.",
      {
        kind: z.enum(["note", "task", "all"]).optional().describe("Filter by kind (default: all)"),
        tag: z.string().optional().describe("Filter by tag"),
        includeDone: z.boolean().optional().describe("Include completed tasks (default: true)"),
      },
      async (args) => {
        const store = await loadStore();
        const kind = args.kind ?? "all";
        const includeDone = args.includeDone ?? true;
        const filtered = store.entries.filter((e) => {
          if (kind !== "all" && e.kind !== kind) return false;
          if (args.tag && !e.tags.includes(args.tag)) return false;
          if (!includeDone && e.done) return false;
          return true;
        });
        if (filtered.length === 0) {
          return { content: [{ type: "text", text: "No entries match those filters." }] };
        }
        const text = filtered.map(formatEntry).join("\n");
        return { content: [{ type: "text", text }] };
      },
    ),

    tool(
      "complete",
      "Mark a task as done by its id prefix (first 8 chars are enough).",
      {
        id: z.string().describe("Entry id or its prefix"),
      },
      async (args) => {
        const store = await loadStore();
        const match = store.entries.find((e) => e.id.startsWith(args.id));
        if (!match) {
          return { content: [{ type: "text", text: `No entry found for id '${args.id}'.` }] };
        }
        if (match.kind !== "task") {
          return { content: [{ type: "text", text: `Entry ${match.id.slice(0, 8)} is a note, not a task.` }] };
        }
        match.done = true;
        await saveStore(store);
        return { content: [{ type: "text", text: `Completed: ${formatEntry(match)}` }] };
      },
    ),

    tool(
      "delete",
      "Delete a note or task by its id prefix.",
      {
        id: z.string().describe("Entry id or its prefix"),
      },
      async (args) => {
        const store = await loadStore();
        const idx = store.entries.findIndex((e) => e.id.startsWith(args.id));
        if (idx === -1) {
          return { content: [{ type: "text", text: `No entry found for id '${args.id}'.` }] };
        }
        const [removed] = store.entries.splice(idx, 1);
        await saveStore(store);
        return { content: [{ type: "text", text: `Deleted: ${formatEntry(removed)}` }] };
      },
    ),
  ],
});

export const notesToolNames = [
  "mcp__notes__add",
  "mcp__notes__list",
  "mcp__notes__complete",
  "mcp__notes__delete",
];
