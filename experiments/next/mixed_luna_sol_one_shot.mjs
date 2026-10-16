#!/usr/bin/env node
// P0e: experiment-only GitHub Copilot Luna parent -> OpenAI Sol leaf
// via experimental additive providers/models in the SAME Copilot SDK session.
// No user files, shell commands, network tools or external effects permitted.
// No retries. Must observe ACTUAL child lifecycle and model selection events.
import { CopilotClient } from "@github/copilot-sdk";

const apiKey = process.env.OPENAI_API_KEY;
const copilotToken = process.env.GITHUB_TOKEN;
if (!apiKey || !copilotToken) {
  console.error("MIXED_BLOCKED: missing Actions OpenAI API key or GitHub token");
  process.exit(1);
}

const expectedChild = "openai-sol/gpt-6.1-sol";
const state = { mainModel:"gpt-6-luna", started:0, completed:0, failed:0, childModels:[], deniedTools:0, otherTools:0, timeline:[] };
const client = new CopilotClient({ gitHubToken: copilotToken, useLoggedInUser: false });
try {
  await client.start();
  const session = await client.createSession({
    model: "gpt-6-luna",
    providers: [{
      name: "openai-sol",
      type: "openai",
      baseUrl: "https://api.openai.com/v1",
      apiKey,
      wireApi: "responses",
    }],
    models: [{
      provider: "openai-sol",
      id: "gpt-6.1-sol",
      wireModel: "gpt-6.1-sol",
      modelId: "gpt-6.1-sol",
      name: "Sol by OpenAI API",
      maxOutputTokens: 1000,
    }],
    customAgents: [{
      name: "sol-check",
      description: "A sole read-only specialist for verifying the numeric proof 8 + 9 = 17. Use when explicitly asked to delegate to sol-check.",
      prompt: "You are a no-tools leaf agent. Confirm 8+9=17. Your entire reply must be SOL_CHILD_OK_17. Do not edit or call tools.",
      tools: [],
      infer: true,
      model: expectedChild,
      reasoningEffort: "low",
    }],
    availableTools: ["task"],
    onPermissionRequest: request => {
      const toolName = String(request.toolName ?? "");
      if (request.managedApprovalRequired) return {kind:"no-result"};
      if ((request.kind === "custom-tool" || request.kind === "mcp") && toolName === "task") return {kind:"approve-once"};
      state.deniedTools++;
      return {kind:"reject",feedback:"P0e permits only a bounded subagent delegation."};
    },
  });
  session.on(ev => {
    if (ev.type === "subagent.started" || ev.type === "subagent.completed" || ev.type === "subagent.failed") {
      const model = String(ev.data?.model ?? "unknown");
      const name = String(ev.data?.agentName ?? "unknown");
      if (ev.type === "subagent.started") state.started++;
      if (ev.type === "subagent.completed") state.completed++;
      if (ev.type === "subagent.failed") state.failed++;
      state.childModels.push(model);
      state.timeline.push({event:ev.type,name,model});
      console.log("CHILD_EVENT",JSON.stringify({event:ev.type,name,model}));
    }
    if (ev.type === "assistant.usage") {
      const model = String(ev.data?.model ?? "unknown");
      console.log("USAGE_EVENT",JSON.stringify({model,hasUsage:!!ev.data?.inputTokens||!!ev.data?.outputTokens}));
    }
  });
  const answer=await session.sendAndWait({
    prompt: "This is a harmless delegation test. You are the GPT-6 Luna main. You MUST use the task subagent tool exactly once to delegate the calculation 8+9 to the named custom agent sol-check. Do not calculate in the main context first. After receiving its response, reply exactly LUNA_GOT_SOL_17 if and only if the leaf reports SOL_CHILD_OK_17. Do not use any other tools.",
  },90000);
  const finalText=String(answer?.data?.content??"").trim();
  console.log("MAIN_EXACT_REPLY:",finalText==="LUNA_GOT_SOL_17"?"PASS":"NOT_MATCHED");
  console.log("SUBAGENT_LIFECYCLE:",JSON.stringify({started:state.started,completed:state.completed,failed:state.failed,models:[...new Set(state.childModels)],deniedTools:state.deniedTools}));
  if (state.started>=1 && state.completed>=1 && state.failed===0 && state.childModels.some(m=>m===expectedChild||m==="gpt-6.1-sol") && finalText==="LUNA_GOT_SOL_17") {
    console.log("MIXED_LUNA_SOL_SDK_PASS: Luna main called Sol leaf using distinct providers in ONE SDK session.");
  } else {
    console.error("MIXED_SDK_INCONCLUSIVE: do not claim provider mixing without observed child model and lifecycle.");
    process.exitCode=1;
  }
} catch(e) {
  const str=String(e?.message??"");
  const kind=/provider|model|unavailable|not found|unsupported/i.test(str)?"runtime_provider_or_model":/permission|auth|403|401/i.test(str)?"authentication_or_policy":/timeout/i.test(str)?"timeout":"unknown_error";
  console.error("MIXED_SDK_BLOCKED:",kind);
  process.exitCode=1;
} finally {
  try {await client.stop();} catch {}
}
