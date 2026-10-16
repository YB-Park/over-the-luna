#!/usr/bin/env node
// P5: two bounded, real-public-source SDK coding attempts:
// uncustomized SDK vs actual selected RC2 plugin with named leaf delegation.
// Quality is graded independently with Python and no model/API credentials.
import { CopilotClient } from "@github/copilot-sdk";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

const repository=process.cwd();
const artifacts=process.env.ARTIFACT_DIR||path.join(os.tmpdir(),"otl-p5");
fs.mkdirSync(artifacts,{recursive:true});
const model="gpt-6-luna";
const pluginId="over-the-luna-next";
const allowedChanges=new Set(["scripts/validate_release.py","scripts/package_release.py",
                              "tests/test_release.py"]);
const toolSet=["view","read_file","grep","glob","edit_file","apply_patch",
               "task","agent/runSubagent"];
const manifest=JSON.parse(fs.readFileSync(path.join(repository,"plugin.json"),"utf8"));
if(manifest.name!==pluginId||manifest.version!=="2.0.0-rc.2")
  throw Error("ACTUAL_PLUGIN_MISMATCH");

function populate(work){
  for(const rel of ["plugin.json","LICENSE","README.md","README.ko.md",
                    "docs/ROLE_TOPOLOGY.md","scripts/validate_release.py",
                    "scripts/package_release.py","tests/test_release.py"]){
    const source=path.join(repository,rel);
    const dest=path.join(work,rel);
    fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(source,dest);
  }
  fs.cpSync(path.join(repository,"agents"),path.join(work,"agents"),{recursive:true});
}

function snapshot(root){
  const out=new Map();
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name==="__pycache__"||entry.name===".git")continue;
      const file=path.join(dir,entry.name);
      if(entry.isDirectory())walk(file);
      else if(entry.isFile()&&!file.endsWith(".pyc")){
        const relative=path.relative(root,file).replaceAll(path.sep,"/");
        out.set(relative,fs.readFileSync(file,"utf8"));
      }
    }
  };
  walk(root);
  return out;
}

function permissions(req,work,log){
  const kind=String(req.kind??"unknown");
  const tool=String(req.toolName??"");
  let result={kind:"reject",feedback:"This comparison allows public-fixture reads, scoped file edits and named subagent delegation only."};
  if(req.managedApprovalRequired){result={kind:"no-result"};}
  else if(kind==="read"){result={kind:"approve-once"};}
  else if(kind==="write"){
    const file=String(req.fileName??"");
    const normalized=path.relative(work,path.resolve(work,file)).replaceAll(path.sep,"/");
    if(allowedChanges.has(normalized))result={kind:"approve-once"};
  } else if((kind==="custom-tool"||kind==="mcp")&&
    (tool==="task"||tool==="agent/runSubagent")){
    result={kind:"approve-once"};
  }
  log.push({kind,tool:tool.slice(0,48),decision:result.kind});
  return result;
}

function runGrader(work){
  const env={PATH:process.env.PATH||"",HOME:os.tmpdir(),
             LANG:"C.UTF-8",PYTHONDONTWRITEBYTECODE:"1"};
  const run=spawnSync("python",[
    path.join(repository,"scripts/role_pipeline_grader.py"),"--work",work
  ],{cwd:work,env,encoding:"utf8",timeout:105000});
  try{
    const line=run.stdout.trim().split("\n").at(-1);
    return {exit:run.status,summary:JSON.parse(line)};
  }catch{
    return {exit:run.status,summary:{pass:false,error:"grader_result_missing"}};
  }
}
const request=[
 "Fix an actual release packaging security issue in this public research repository.",
 "The plugin ZIP builder scripts/package_release.py reads and archives allowlisted",
 "files using .read_bytes(). A symlink such as README.md -> outside-of-plugin data",
 "or agents/over-the-luna-next.agent.md -> outside may be accepted by",
 "scripts/validate_release.py, leaking file content into the ZIP.",
 "Preserve legitimate plugin packaging while rejecting symlinks escaping the",
 "plugin boundary. Prefer rejecting ANY symlink in allowlisted source paths",
 "and ensure packaging fails closed. Examine the cross-module contract among",
 "scripts/validate_release.py, scripts/package_release.py and tests/test_release.py.",
 "Add independent regression tests for a valid ordinary plugin and for symlinked",
 "README, LICENSE and agent paths. Prove validator AND packager reject invalid",
 "candidates; preserve deterministic ZIP behavior and prior role constraints.",
 "Change only scripts/validate_release.py, scripts/package_release.py",
 "and tests/test_release.py. No shell/test-runner, git, web, remote or secrets",
 "tools are available in this controlled SDK run. CI externally executes",
 "your authored regression tests and hidden acceptance mutations.",
 "Do not claim tests ran if you could not execute them; do not push or publish."
].join(" ");
const specific=request+" This task requires discovering the validation-to-package "+
  "dependency and separately reviewing the consequential data-leak invariant. "+
  "As the selected Over the Luna Next Main, FIRST delegate one bounded repository "+
  "contract discovery to named Next Architect (not generic explore). After editing, "+
  "delegate one independent review to named Next Reviewer and supply actual changed "+
  "files and real diff hunks; no manufactured artifact, no unrelated role. "+
  "You may not run shell commands yourself in this harness; the external CI "+
  "validator will run tests. If real diff/patch or proper delegation tool is "+
  "unavailable, report that honestly rather than claiming Reviewer PASS.";

if(!process.env.GITHUB_TOKEN)throw Error("GitHub Actions authorized token missing");
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,
  useLoggedInUser:false,enableConfigDiscovery:false});
const summary={schema:1,repoSha:process.env.GITHUB_SHA||"unknown",
 model, sdk:"@github/copilot-sdk@1.0.19",cli:"@github/copilot@1.0.88",
 test:"public real plugin packaging symlink leak (Main/Architect/Reviewer)",
 arms:[]};
let invalidRuntime=false;
try{
 await client.start();
 for(const mode of ["sdk_default","rc2_actual_plugin"]){
  const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-p5-"+mode+"-"));
  populate(work);
  const before=snapshot(work);
  const permissionsLog=[],events=[],usage=[];
  const config={model,reasoningEffort:"low",workingDirectory:work,
    pluginDirectories:mode==="rc2_actual_plugin"?[repository]:[],
    availableTools:toolSet,enableSessionStore:false,
    onPermissionRequest:r=>permissions(r,work,permissionsLog)};
  let session,error=null,pluginLoaded=false,mainSelected=false;
  let started=Date.now();
  try{
    session=await client.createSession(config);
    const plugins=await session.rpc.plugins.list();
    pluginLoaded=(plugins.plugins||[]).some(x=>x.name===pluginId&&x.enabled!==false);
    if(mode==="rc2_actual_plugin"){
      if(!pluginLoaded)throw Error("PLUGIN_NOT_LOADED");
      const res=await session.rpc.agent.list();
      const named=(res.agents||[]).find(x=>x.displayName==="Over the Luna Next"&&
                                      String(x.name).startsWith(pluginId+":"));
      if(!named)throw Error("MAIN_AGENT_NOT_FOUND");
      await session.rpc.agent.select({name:named.name});
      const current=await session.rpc.agent.getCurrent();
      mainSelected=(current.agent?.name??current.name)===named.name;
      if(!mainSelected)throw Error("MAIN_NOT_SELECTED");
    }else if(pluginLoaded){throw Error("DEFAULT_CONTAMINATED_BY_PLUGIN");}
    session.on(e=>{
      if(e.type==="assistant.usage"){
        const d=e.data||{};
        usage.push({model:String(d.model||"unknown"),
          inputTokens:d.inputTokens??0,outputTokens:d.outputTokens??0,
          copilotNanoAiu:d.copilotUsage?.totalNanoAiu??null});
      }
      if(e.type.startsWith("subagent.")){
        events.push({type:e.type,name:String(e.data?.agentDisplayName||
          e.data?.agentName||""),model:String(e.data?.model||"unobserved"),
          toolCallId:String(e.data?.toolCallId||"").slice(0,72)});
      }
      if(e.type==="assistant.tool_call"||e.type.startsWith("tool."))
        events.push({type:e.type,name:String(e.data?.toolName||
          e.data?.name||"").slice(0,60)});
    });
    await session.sendAndWait({prompt:mode==="rc2_actual_plugin"?specific:request},115000);
  }catch(e){
    const s=String(e?.message||"");
    error=/timeout/i.test(s)?"timeout":/policy|model|permission|auth|plugin/i.test(s)?
      "environment_or_policy":"runtime_error";
    console.log("P5_ERROR",JSON.stringify({mode,error,message:s.slice(0,200)}));
    invalidRuntime=true;
  }finally{try{await session?.disconnect()}catch{}}
  const durationMs=Date.now()-started;
  const after=snapshot(work);
  const changed=[...new Set([...before.keys(),...after.keys()])]
      .filter(n=>before.get(n)!==after.get(n)).sort();
  const unexpected=changed.filter(n=>!allowedChanges.has(n));
  const grade=runGrader(work);
  const observed=usage.some(x=>x.model===model);
  const subagentStarts=events.filter(x=>x.type==="subagent.started");
  const subagentCompleted=events.filter(x=>x.type==="subagent.completed");
  const hasRole=(n)=>subagentStarts.some(x=>x.name===n)&&
     subagentCompleted.some(x=>x.name===n);
  const roleChain=mode==="rc2_actual_plugin"?
     hasRole("Next Architect")&&hasRole("Next Reviewer"):null;
  const acceptance=!!grade.summary.pass&&grade.exit===0&&unexpected.length===0&&
    observed&&!error&&(mode==="sdk_default"||pluginLoaded&&mainSelected);
  const rec={mode,acceptance,roleChain,pluginLoaded,mainSelected,
    architectObserved:hasRole("Next Architect"),reviewerObserved:hasRole("Next Reviewer"),
    subagentStarts,subagentCompleted,durationMs,usage,permissionAudit:permissionsLog,
    events:events.slice(0,130),changedPaths:changed,unexpectedPaths:unexpected,
    grading:grade.summary,modelObserved:observed,error};
  const out=path.join(artifacts,mode);
  fs.mkdirSync(out,{recursive:true});
  for(const file of allowedChanges){
    if(after.has(file)){
      const target=path.join(out,file);
      fs.mkdirSync(path.dirname(target),{recursive:true});
      fs.writeFileSync(target,after.get(file));
    }
  }
  summary.arms.push(rec);
  console.log("P5_ARM",JSON.stringify({mode,accepted:acceptance,roleChain,
   architect:rec.architectObserved,reviewer:rec.reviewerObserved,changed,unexpected,
   tests:grade.summary.num_user_tests||0,failed:grade.summary.failed_checks||[],
   inputTokens:usage.reduce((n,u)=>n+u.inputTokens,0),
   outputTokens:usage.reduce((n,u)=>n+u.outputTokens,0),durationMs,error}));
  if(error||!observed)break;
 }
}finally{
 try{await client.stop()}catch{}
 fs.writeFileSync(path.join(artifacts,"summary.json"),JSON.stringify(summary,null,2));
}
const finished=summary.arms.length===2;
console.log("P5_EVALUATION",JSON.stringify({completed:finished,
  arms:summary.arms.map(a=>({mode:a.mode,quality:a.acceptance,
    actualRoleChain:a.roleChain,roles:{architect:a.architectObserved,
      reviewer:a.reviewerObserved}}))}));
if(!finished||invalidRuntime)process.exitCode=1;
// Quality and missing roles are reported as outcomes, not green-CI proof.
