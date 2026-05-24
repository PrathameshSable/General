import "dotenv/config";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";
import { agentOptions } from "./agent.js";

async function main(): Promise<void> {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.");
    process.exit(1);
  }

  const rl = readline.createInterface({ input, output });
  rl.on("close", () => process.exit(0));

  console.log("Personal assistant ready. Type a message, or 'exit' to quit.\n");

  // Queue lets us push user turns into the SDK's streaming-input mode while
  // the agent processes the current turn.
  const pending: SDKUserMessage[] = [];
  let resolveNext: ((msg: SDKUserMessage | null) => void) | null = null;
  let finished = false;

  function pushUserMessage(text: string): void {
    const msg: SDKUserMessage = {
      type: "user",
      message: { role: "user", content: text },
      parent_tool_use_id: null,
      session_id: "cli",
    };
    if (resolveNext) {
      const r = resolveNext;
      resolveNext = null;
      r(msg);
    } else {
      pending.push(msg);
    }
  }

  async function* userStream(): AsyncGenerator<SDKUserMessage> {
    while (!finished) {
      if (pending.length > 0) {
        yield pending.shift()!;
        continue;
      }
      const next = await new Promise<SDKUserMessage | null>((r) => {
        resolveNext = r;
      });
      if (next === null) return;
      yield next;
    }
  }

  // Prompt loop runs in parallel with the agent loop.
  const promptLoop = (async () => {
    while (true) {
      const line = (await rl.question("you> ")).trim();
      if (!line) continue;
      if (line === "exit" || line === "quit") {
        finished = true;
        const r = resolveNext as ((msg: SDKUserMessage | null) => void) | null;
        resolveNext = null;
        if (r) r(null);
        rl.close();
        return;
      }
      pushUserMessage(line);
    }
  })();

  try {
    for await (const message of query({ prompt: userStream(), options: agentOptions })) {
      if (message.type === "assistant") {
        process.stdout.write("\nassistant> ");
        for (const block of message.message.content) {
          if (block.type === "text") {
            process.stdout.write(block.text);
          }
        }
        process.stdout.write("\n\n");
      } else if (message.type === "result" && message.subtype !== "success") {
        console.error(`\n[agent ended: ${message.subtype}]`);
        break;
      }
    }
  } finally {
    finished = true;
    rl.close();
    await promptLoop.catch(() => {});
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
