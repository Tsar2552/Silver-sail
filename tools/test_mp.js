// ทดสอบตรรกะเล่นหลายคนด้วยเครือข่ายจำลองในหน่วยความจำ: node tools/test_mp.js [รอบ]
const fs=require("fs"),path=require("path");const rd=n=>JSON.parse(fs.readFileSync(path.join(__dirname,"..","data",n),"utf8"));
const mem={};globalThis.localStorage={getItem:k=>mem[k]??null,setItem:(k,v)=>{mem[k]=v}};
const {Vault,Campaign}=require("../js/vault.js");globalThis.Vault=Vault;globalThis.Campaign=Campaign;
globalThis.Battle=require("../js/battle.js");const Story=require("../js/story.js");const MP=require("../js/mp.js");
const D={monsters:rd("monsters.json"),weapons:rd("weapons.json"),armor:rd("armor.json"),items:rd("items.json"),act1:rd("story/act1.json")};
const rnd=n=>Math.floor(Math.random()*n),d20=()=>1+rnd(20);
const mkV=(tag,stats)=>({bg(){},status(l){this.last=l;},toast(){},
  say:(n,o)=>o.wait?Promise.resolve():undefined,
  choice(n,o){if(o.canVote)setTimeout(()=>o.onPick(rnd(3)),0);return{tally(v,t){stats.tallies++;},lock(){},result(t){stats.results++;if(t.includes("เสมอ"))stats.ties++;}};},
  check(n,v,o){if(o.canRoll)setTimeout(o.onConfirm,0);return{waiting(){}};},checkResult:()=>Promise.resolve(),
  shop(t,l,o){if(o.canShop)setTimeout(()=>{o.onBuy("potion");o.onBuy("potion");o.onDone();},0);return{update(){},close(){}};},
  battleStart(){},battleLog(){},battleRefresh(){},battleEnd(){},
  battleMenu({Ps,Es,idx,inv,round},o){const E=Es.find(e=>e.hp>0),P=Ps[idx];setTimeout(()=>o.onAct(E.boss&&E.charge===2?"guard":P.hp<P.maxhp*.4&&inv.pot>0?"potion":inv.fire?"fire":"heavy"),0);},
  battleWait(){},end(){stats.ends++;return Promise.resolve();}});
async function one(nPlayers,hostPlays,stats){
  Object.keys(mem).forEach(k=>delete mem[k]);
  const names=hostPlays?["โฮสต์"]:[];for(let i=hostPlays?1:0;i<nPlayers;i++)names.push("P"+i);
  const hostName=hostPlays?"โฮสต์":"GM";
  const camp=Campaign.create("t",hostName,"multi");
  names.forEach(n=>{const c=Vault.create({name:"ตัว"+n,stats:{hp:130,p_atk:3,m_atk:2,p_def:2,m_def:2,spd:5,luck:1,wit:10,mana:20}});Campaign.addMember(camp,n,Vault.checkout(c.cid,"t"));});
  // เครือข่ายจำลอง
  const clients=new Map(),hostHandlers={msg:[],leave:[]};
  const T={broadcast:m=>clients.forEach(c=>setTimeout(()=>c.fn&&c.fn(JSON.parse(JSON.stringify(m))),0)),send:(o,m)=>{const c=clients.get(o);c&&setTimeout(()=>c.fn&&c.fn(JSON.parse(JSON.stringify(m))),0);},
    onMsg:f=>hostHandlers.msg.push(f),onLeave:f=>hostHandlers.leave.push(f),owners:()=>[...clients.keys()]};
  const ui=MP.makeHostUI(mkV("host",stats),T,{hostName,rng:d20,delay:0,getState:()=>g.getState()});
  const g=await Story.start({data:D,campId:camp.id});Story.setUI(ui);
  names.filter(n=>n!==hostName).forEach(n=>{const c={fn:null};clients.set(n,c);
    MP.makeClient(mkV(n,stats),{send:m=>setTimeout(()=>hostHandlers.msg.forEach(f=>f(n,JSON.parse(JSON.stringify(m)))),0),onMsg:f=>{c.fn=f;}},{name:n});});
  await Promise.race([g.run(),new Promise((_,rj)=>setTimeout(()=>rj(new Error("ค้าง")),8000))]);
}
(async()=>{const N=+process.argv[2]||40;const stats={tallies:0,results:0,ties:0,ends:0};let fail=0;
  for(const [n,hp] of [[2,true],[3,true],[4,true],[3,false],[2,false]]){let ok=0;const before=stats.ends;
    for(let i=0;i<N;i++){try{await one(n,hp,stats);ok++;}catch(e){fail++;console.log("FAIL",n,hp,e.message);}}
    console.log(`${n} ผู้เล่น ${hp?"(Host เล่นด้วย)":"(Host เป็นผู้ดูแล)"}: จบ ${ok}/${N}`);}
  console.log("โหวตสรุป",stats.results,"ครั้ง | เสมอ→ทอย",stats.ties,"ครั้ง");process.exit(fail?1:0);})();
