#!/usr/bin/env node
// Read-only model catalogue discovery. Creates NO LLM session and sends NO prompt.
import { CopilotClient } from "@github/copilot-sdk";

const target = ["gpt-6-luna", "claude-haiku-5.5", "gpt-6.1-sol", "claude-sonnet-5.5"];
const client = new CopilotClient();
try {
  await client.start();
  const response = await client.listModels();
  const models = Array.isArray(response) ? response : (response.models ?? []);
  console.log("SDK_MODEL_CATALOG_COUNT:", models.length);
  for (const id of target) {
    const m = models.find(x => String(x.id ?? "").toLowerCase() === id);
    const effort = m?.capabilities?.supports?.reasoningEffort;
    console.log(JSON.stringify({
      requested: id,
      listed: !!m,
      reasoningEffortSupported: typeof effort === "boolean" ? effort : "unknown",
    }));
  }
  // Absence is a discovery result, not an inference performance score.
  if (models.length === 0) {
    console.log("INCONCLUSIVE: SDK model list is empty; check account/policy.");
    process.exitCode = 1;
  }
} catch (e) {
  console.error("MODEL_CATALOG_BLOCKED:", e?.message ?? String(e));
  process.exitCode = 1;
} finally {
  await client.stop();
}
