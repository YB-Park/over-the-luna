#!/usr/bin/env node
// P4: ACTUAL plugin loaded and selected (not copied instructions). SDK, not VS Code.
// SAME Luna model, tool policy and tiny public fixture; only the
// system-message APPEND uses the actual candidate instruction body.
// At most TWO billable model sessions, no retries, no shell/network tools.
import { CopilotClient } from "@github/copilot-sdk";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

const root = process.cwd();
const resultDir = process.env.RESULT_DIR || path.join(os.tmpdir(), "otl-actual-plugin-pair");
fs.mkdirSync(resultDir, { recursive: true });
const pluginDir=path.join(root,"experiments/next/candidate-plugin");
const pluginManifest=JSON.parse(fs.readFileSync(path.join(pluginDir,"plugin.json"),"utf8"));
if(pluginManifest.name!=="over-the-luna-next")throw new Error("PLUGIN_MANIFEST_MISMATCH");
const tools = ["view", "read_file", "edit_file", "apply_patch", "grep", "glob"];
const allowed = new Set(["scripts/validate_candidate.py","tests/test_validate_candidate.py"]);
const model = "gpt-6-luna";

function source(src, dst) {
  fs.mkdirSync(path.dirname(dst), {recursive:true});
  fs.copyFileSync(src,dst);
}
function populate(dir) {
  source(path.join(root,"scripts/validate_candidate.py"),path.join(dir,"scripts/validate_candidate.py"));
  const sourceCandidate=path.join(root,"experiments/next/candidate-plugin");
  const dest=path.join(dir,"experiments/next/candidate-plugin");
  fs.cpSync(sourceCandidate,dest,{recursive:true});
  fs.mkdirSync(path.join(dir,"tests"),{recursive:true});
  source(path.join(root,"tests/test_validate_candidate.py"),path.join(dir,"tests/test_validate_candidate.py"));
}
function filesIn(dir) {
  const output=new Map();
  function walk(loc) {
    for(const item of fs.readdirSync(loc,{withFileTypes:true})) {
      if(item.name==="__pycache__" || item.name===".git")continue;
      const abs=path.join(loc,item.name);
      if(item.isDirectory())walk(abs);
      else if(item.isFile()&&!item.name.endsWith(".pyc")){
        const name=path.relative(dir,abs).replaceAll(path.sep,"/");
        output.set(name,fs.readFileSync(abs,"utf8"));
      }
    }
  }
  walk(dir);
  return output;
}
function sanitizedExec(work) {
  const env={PATH:process.env.PATH,HOME:process.env.RUNNER_TEMP||os.tmpdir(),
    LANG:"C.UTF-8",LC_ALL:"C.UTF-8",PYTHONDONTWRITEBYTECODE:"1"};
  return spawnSync("python",[path.join(root,"experiments/next/actual_plugin_code_grader.py"),"--work",work],
   {encoding:"utf8",cwd:work,env,timeout:100000});
}
function usageRecord(ev) {
  const d=ev.data||{};
  return {model:String(d.model||"unknown"),isByok:!!d.isByok,
    inputTokens:d.inputTokens??null,outputTokens:d.outputTokens??null,
    cachedInputTokens:d.cacheReadTokens??null,
    copilotNanoAiu:d.copilotUsage?.totalNanoAiu??null};
}
function denyOrApprove(req,work,audit) {
  const kind=String(req.kind||"unknown");
  const tool=String(req.toolName||"");
  let decision={kind:"reject",feedback:"Only read/search and two explicitly scoped fixture writes are allowed."};
  const managed=!!req.managedApprovalRequired;
  if(managed) decision={kind:"no-result"};
  else if(kind==="read") {
    // SDK read approvals may omit fileName for view/glob/rg operations.
    // This workflow contains only a public, disposable fixture, exposes no
    // shell/network tool, and grants no secrets to external graders.
    // Restricting reads via fileName silently rejected ALL reads on P2 attempt 1.
    decision={kind:"approve-once"};
  } else if(kind==="write") {
    const file=req.fileName==null?"":String(req.fileName);
    const effective=path.resolve(work,file);
    const relative=path.relative(work,effective).replaceAll(path.sep,"/");
    if(allowed.has(relative)) decision={kind:"approve-once"};
  } else if((kind==="custom-tool"||kind==="mcp")&&tools.includes(tool)){
    decision={kind:"approve-once"};
  }
  audit.push({kind,tool:tool.slice(0,40),decision:decision.kind});
  return decision;
}
const task=[
 "Improve the actual research candidate static validator, scripts/validate_candidate.py.",
 "We verified that plugin directories load agents/*.md, not just *.agent.md.",
 "The current validator only globs agents/*.agent.md and silently accepts a second",
 "agents/reviewer.md. Correct this security-relevant false negative:",
 "the agents directory must contain EXACTLY the existing approved over-the-luna-next.agent.md",
 "file and no other agent Markdown (*.md) files.",
 "Also reject any plugin-bundled skills directory containing SKILL.md; Next should have no skills.",
 "Extend the existing stdlib regression tests in tests/test_validate_candidate.py:",
 "pristine candidate PASS; agents/reviewer.md FAIL; skills/audit/SKILL.md FAIL;",
 "and preserve all previous negative mutation coverage.",
 "Only modify scripts/validate_candidate.py and tests/test_validate_candidate.py.",
 "Do not alter the candidate plugin, original 1.1.1, or other repo files.",
 "You have read/search/patch tools but NO shell/test-runner or git/network tools.",
 "Host CI, without API credentials, will execute the new regression tests and",
 "an independent grader after the turn. Do not claim tests ran in your environment.",
 "Do not ask for permission to extend scope; no subagents, commits, pushes or external effects."
].join(" ");

if(!process.env.GITHUB_TOKEN)throw new Error("GITHUB_TOKEN missing in authorized Actions job");
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,useLoggedInUser:false,
  enableConfigDiscovery:false});
const strategies=["actual_next_plugin","sdk_default"];
const output={timestamp:"2026-10-16",schema:1,method:"SDK only: actual selected plugin agent vs default SDK, independently graded real source fix",
  model,reasoningEffort:"low",toolAllowlist:tools,repoCommit:process.env.GITHUB_SHA||"unknown",
  pluginManifest:pluginManifest.name,
  environment:{sdk:"@github/copilot-sdk@1.0.19",cli:"@github/copilot@1.0.88"},
  results:[]};
let infraFailure=false;
try{
 await client.start();
 for(const strategy of strategies){
  const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-actions-"+strategy+"-"));
  populate(work);
  const initial=filesIn(work);
  const audit=[], usage=[], toolEvents=[];
  const config={model,reasoningEffort:"low",workingDirectory:work,
    availableTools:tools,enableSessionStore:false,skillDirectories:[],
    onPermissionRequest:r=>denyOrApprove(r,work,audit)};
  if(strategy==="actual_next_plugin")
    config.pluginDirectories=[pluginDir];
  else config.pluginDirectories=[];
  let session, error=null, pluginLoaded=false,agentSelected=false;
  let selectionEvidence={};
  // Metadata registration and selection must succeed BEFORE model inference.
  // For the default SDK arm, the Next plugin must NOT bleed into that session.
  const began=Date.now();
  try {
    session=await client.createSession(config);
    const registry=await session.rpc.plugins.list();
    const pluginNames=(registry?.plugins??[]).filter(x=>x.enabled!==false).map(x=>x.name);
    pluginLoaded=pluginNames.includes(pluginManifest.name);
    if(strategy==="actual_next_plugin"){
      if(!pluginLoaded)throw new Error("PLUGIN_NOT_LOADED");
      const agentRegistry=await session.rpc.agent.list();
      const agents=agentRegistry?.agents??[];
      const item=agents.find(x=>String(x.name??"").startsWith("over-the-luna-next:")&&
        String(x.displayName??"").includes("Over the Luna Next"));
      if(!item)throw new Error("PLUGIN_AGENT_NOT_FOUND");
      await session.rpc.agent.select({name:item.name});
      const selected=await session.rpc.agent.getCurrent();
      const name=String(selected?.agent?.name??selected?.current?.name??selected?.name??"");
      agentSelected=name===item.name;
      selectionEvidence={plugin:item.name.split(":")[0],selectedName:name};
      if(!agentSelected)throw new Error("PLUGIN_AGENT_NOT_SELECTED");
    }else{
      if(pluginLoaded)throw new Error("DEFAULT_CONTAMINATED_BY_PLUGIN");
      const current=await session.rpc.agent.getCurrent();
      if(current?.agent||current?.name)throw new Error("DEFAULT_HAS_CUSTOM_AGENT");
    }
    session.on(ev=>{
      if(ev.type==="assistant.usage") usage.push(usageRecord(ev));
      if(ev.type==="assistant.tool_call"||ev.type.startsWith("tool."))
        toolEvents.push({type:ev.type,tool:String(ev.data?.toolName||ev.data?.name||"unknown").slice(0,48)});
    });
    await session.sendAndWait({prompt:task},105000);
  }catch(e) {
    const msg=String(e?.message||"");
    error=/timeout/i.test(msg)?"timeout":/model|permission|provider|auth|policy/i.test(msg)?"access_or_policy":"runtime_error";
    infraFailure=true;
  }finally{if(session)try{await session.disconnect();}catch{}}
  const elapsedMs=Date.now()-began;
  const after=filesIn(work);
  const changed=[...new Set([...initial.keys(),...after.keys()])]
    .filter(p=>initial.get(p)!==after.get(p)).sort();
  const unexpected=changed.filter(p=>!allowed.has(p));
  const check=sanitizedExec(work);
  let grade={pass:false,failed_check_names:["grader_no_result"]};
  const gradeLine=check.stdout?.split("\n").filter(Boolean).at(-1);
  try{grade=JSON.parse(gradeLine)}catch{}
  const observed=usage.map(x=>x.model);
  const realModelSeen=observed.includes(model);
  const fullPass=!error&&check.status===0&&grade.pass===true&&
    unexpected.length===0&&realModelSeen&&
    (strategy==="actual_next_plugin"?pluginLoaded&&agentSelected:!pluginLoaded);
  const tokenIn=usage.reduce((n,x)=>n+(x.inputTokens||0),0);
  const tokenOut=usage.reduce((n,x)=>n+(x.outputTokens||0),0);
  const rec={strategy,fullPass,gradePass:grade.pass===true,checks:grade.checks||{},
    graderFailures:grade.failed_check_names||[],testCount:grade.num_user_tests||0,
    changedPaths:changed,unexpectedPaths:unexpected,elapsedMs,inputTokens:tokenIn,
    outputTokens:tokenOut,modelSeen:realModelSeen,usage,permissionAudit:audit,
    toolEvents:toolEvents.slice(0,75),pluginLoaded,agentSelected,selectionEvidence,error};
  output.results.push(rec);
  // Save complete public source/test files for independently reviewing results.
  const armDir=path.join(resultDir,strategy);
  fs.mkdirSync(armDir,{recursive:true});
  for(const file of allowed){
    const content=after.get(file);
    if(typeof content==="string"){
      const dest=path.join(armDir,file);
      fs.mkdirSync(path.dirname(dest),{recursive:true});
      fs.writeFileSync(dest,content);
    }
  }
  console.log("DOGFOOD_ARM",JSON.stringify({strategy,fullPass,gradePass:rec.gradePass,
    testCount:rec.testCount,failedChecks:rec.graderFailures,changedPaths:changed,
    unexpectedPaths:unexpected,modelSeen:realModelSeen,pluginLoaded,agentSelected,inputTokens:tokenIn,
    outputTokens:tokenOut,elapsedMs,error}));
  if(error||!realModelSeen)break;
 }
}finally{
 try{await client.stop();}catch{}
 fs.writeFileSync(path.join(resultDir,"results.json"),JSON.stringify(output,null,2));
}
const done=output.results.length===2;
console.log("DOGFOOD_SUMMARY",JSON.stringify({complete:done,
  arms:output.results.map(x=>({strategy:x.strategy,quality:x.fullPass,changed:x.changedPaths.length,
  failures:x.graderFailures.length})),status:!done||infraFailure?"INCONCLUSIVE":"COMPLETED_EVAL"}));
if(!done||infraFailure)process.exitCode=1;
// A completed experiment can succeed in CI even if an arm fails quality.
// Grading is retained as data, not conflated with infrastructure.
