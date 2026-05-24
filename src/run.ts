import "dotenv/config";
import { query } from "@anthropic-ai/claude-agent-sdk";
import { agentOptions } from "./agent.js";

async function main(): Promise<void> {
  const prompt = process.argv.slice(2).join(" ").trim();
  if (!prompt) {
    console.error('Usage: npm run ask -- "your question here"');
    process.exit(1);
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.");
    process.exit(1);
  }

  for await (const message of query({ prompt, options: agentOptions })) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if (block.type === "text") {
          process.stdout.write(block.text);
        }
      }
      process.stdout.write("\n");
    } else if (message.type === "result") {
      if (message.subtype !== "success") {
        console.error(`\n[agent ended: ${message.subtype}]`);
        process.exit(1);
      }
    }
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
