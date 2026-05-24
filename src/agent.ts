import type { Options } from "@anthropic-ai/claude-agent-sdk";
import { notesServer, notesToolNames } from "./tools/notes.js";

const SYSTEM_PROMPT = `You are a personal assistant agent for the user.

You can help with:
- General questions and conversation
- Reading, writing, and editing files in the current project
- Running shell commands when needed
- Searching and fetching content from the web
- Keeping track of the user's notes and tasks in a local store

When the user asks you to remember something, save a thought, or track a todo,
use the notes tools (mcp__notes__*). Prefer 'task' kind for actionable items
and 'note' kind for free-form information.

Be concise. When you take an action, briefly say what you did. Don't narrate
every internal step — just the outcome.

When editing files or running commands, work in the user's current directory
unless they specify otherwise.`;

const DEFAULT_MODEL = process.env.CLONE_AGENT_MODEL ?? "claude-opus-4-7";

export const agentOptions: Options = {
  model: DEFAULT_MODEL,
  systemPrompt: SYSTEM_PROMPT,
  mcpServers: {
    notes: notesServer,
  },
  allowedTools: [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
    "WebFetch",
    "WebSearch",
    ...notesToolNames,
  ],
  permissionMode: "acceptEdits",
};
