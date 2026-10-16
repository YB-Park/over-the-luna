#!/usr/bin/env node
// One paired GitHub Actions SDK study, not a VS Code Agent Host test.
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
const resultDir = process.env.RESULT_DIR || path.join(os.tmpdir(), "otl-action-pair");
fs.mkdirSync(resultDir, { recursive: true });
const agentPath = path.join(root, "experiments/next/candidate-plugin/agents/over-the-luna-next.agent.md");
const candidateFile = fs.readFileSync(agentPath, "utf8");
const parts = candidateFile.split(/\r?\n---\r?\n/);
if (!candidateFile.startsWith("---\n") || parts.length < 2)
  throw new Error("ACTUAL_CANDIDATE_FRONTMATTER_NOT_FOUND");
const candidateInstructions = parts.slice(1).join("\n---\n").trim();
if (candidateInstructions.length < 800 || !candidateInstructions.includes("Run the tests you claim passed"))
  throw new Error("CANDIDATE_INSTRUCTIONS_INVALID");
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
  return spawnSync("python",[path.join(root,"experiments/next/action_pair_grader.py"),"--work",work],
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
    // Approve an SDK read within this public temporary fixture only.
    const file=req.fileName==null?"":String(req.fileName);
    const effective=path.resolve(work,file);
    const relative=path.relative(work,effective).replaceAll(path.sep,"/");
    if(relative && !relative.startsWith("../") && !path.isAbsolute(relative))
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
const task = [
"Improve the ACTUAL research candidate validator scripts/validate_candidate.py.",
"Add optional --root PATH to validate the specified candidate plugin directory;",
"when omitted, the current default behavior must remain intact.",
"Add tests/test_validate_candidate.py using standard-library unittest and",
"temporary copies of experiments/next/candidate-plugin. Check pristine plugin PASS,",
"and reject each: tools: [] injected in Main, a pinned model: value in Main,",
"an additional *.agent.md leaf, missing/invalid plugin.json, bundled .mcp.json or mcp.json.",
"Do not modify any other paths or the actual candidate plugin files.",
"Use file-reading and patch/edit tools only; you have NO shell, terminal or test-runner tool.",
"The CI host will execute your modified tests and independently grade behavior after this turn.",
"Do not claim tests passed unless you executed them. Make useful, real file edits.",
"Do not commit, push, publish, use subagents, or call external services."
].join(" ");

if(!process.env.GITHUB_TOKEN)throw new Error("GITHUB_TOKEN missing in authorized Actions job");
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,useLoggedInUser:false,
  enableConfigDiscovery:false});
const strategies=["sdk_default","next_instructions"];
const output={timestamp:"2026-10-16",schema:1,method:"SDK only: default instructions vs append actual Next candidate body",
  model,reasoningEffort:"low",toolAllowlist:tools,repoCommit:process.env.GITHUB_SHA||"unknown",
  instructionsSha256:crypto.createHash("sha256").update(candidateInstructions).digest("hex"),
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
  if(strategy==="next_instructions"){
    config.systemMessage={mode:"append",content:candidateInstructions};
  }
  let session, error=null;
  const began=Date.now();
  try {
    session=await client.createSession(config);
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
    unexpected.length===0&&realModelSeen;
  const tokenIn=usage.reduce((n,x)=>n+(x.inputTokens||0),0);
  const tokenOut=usage.reduce((n,x)=>n+(x.outputTokens||0),0);
  const rec={strategy,fullPass,gradePass:grade.pass===true,checks:grade.checks||{},
    graderFailures:grade.failed_check_names||[],testCount:grade.num_user_tests||0,
    changedPaths:changed,unexpectedPaths:unexpected,elapsedMs,inputTokens:tokenIn,
    outputTokens:tokenOut,modelSeen:realModelSeen,usage,permissionAudit:audit,
    toolEvents:toolEvents.slice(0,75),error};
  output.results.push(rec);
  // Save both complete candidate files, not just paths, to permit later diff review.
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
    unexpectedPaths:unexpected,modelSeen:realModelSeen,inputTokens:tokenIn,
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
