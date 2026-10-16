#!/usr/bin/env node
// P0d: one isolated Copilot SDK session over OpenAI Responses BYOK.
// This script has no retry loop, no custom tools, and rejects all permissions.
import { CopilotClient } from "@github/copilot-sdk";

const key = process.env.OPENAI_API_KEY;
if (!key) {
  console.error("SDK_SOL_BLOCKED: OPENAI_API_KEY is empty or unavailable");
  process.exit(1);
}

const client = new CopilotClient();
try {
  await client.start();
  const session = await client.createSession({
    model: "gpt-6.1-sol",
    reasoningEffort: "low",
    provider: {
      type: "openai",
      baseUrl: "https://api.openai.com/v1",
      apiKey: key,
      wireApi: "responses",
    },
    tools: [],
    onPermissionRequest: () => ({
      kind: "reject",
      feedback: "All tool calls are prohibited in this isolated smoke test.",
    }),
  });
  const finalMessage = await session.sendAndWait(
    { prompt: "Respond with exactly SDK_SOL_OK. Do not invoke tools." },
    55000
  );
  const answer = String(finalMessage?.data?.content ?? "").trim();
  if (answer !== "SDK_SOL_OK") {
    console.error("SDK_SOL_INCONCLUSIVE: expected exact short reply was not returned");
    process.exitCode = 1;
  } else {
    console.log("SDK_OPENAI_SOL_BYOK_PASS: exact response from explicitly configured Sol provider session");
    console.log("MODEL_ID_EVIDENCE: configured= gpt-6.1-sol ; no independent provider-side per-request trace captured");
    console.log("COST_EVIDENCE: UNKNOWN; consult OpenAI API usage dashboard");
  }
} catch (error) {
  // Never echo an error object with provider URLs or request payloads.
  const message = String(error?.message ?? "");
  const category = /balance|credit|quota|429/i.test(message)
    ? "billing_or_rate_limit"
    : /401|403|auth|permission|forbidden|policy/i.test(message)
      ? "access_or_policy"
      : "sdk_runtime_or_provider";
  console.error("SDK_SOL_BLOCKED: " + category);
  process.exitCode = 1;
} finally {
  try { await client.stop(); } catch { /* retain original result */ }
}
