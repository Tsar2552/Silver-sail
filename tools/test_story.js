// เดินเนื้อเรื่อง Act 1 อัตโนมัติ (เลือกสุ่ม) หลายร้อยรอบ: ต้องถึงตอนจบ ไม่ค้าง ไม่ error
// node tools/test_story.js [รอบ]
const fs=require("fs"),path=require("path");const rd=n=>JSON.parse(fs.readFileSync(path.join(__dirname,"..","data",n),"utf8"));
const mem={};globalThis.localStorage={getItem:k=>mem[k]??null,setItem:(k,v)=>{mem[k]=v}};
const {Vault,Campaign}=require("../js/vault.js");globalThis.Vault=Vault;globalThis.Campaign=Campaign;
globalThis.Battle=require("../js/battle.js");const Story=require("../js/story.js");
const D={monsters:rd("monsters.json"),weapons:rd("weapons.json"),armor:rd("armor.json"),items:rd("items.json"),npcs:rd("npcs.json"),locations:rd("locations.json"),act1:rd("story/act1.json")};
const N=+process.argv[2]||300;let ended=0,errs=[],stat={wins:0,losses:0,lv:0,gas:0,long:0};const visited=new Set(),flags={};
const pol=(mode)=>({
 async say(n){visited.add(n.id);},bg(){},status(){},toast(){},battleEnd(){},battleStart(){},battleRefresh(){},battleLog(){},
 async choice(n){visited.add(n.id);return Math.floor(Math.random()*3);},
 async check(n,val,rng){visited.add(n.id);const d=rng();return d===20||(d!==1&&d+val>=n.dc);},
 async shop(n,ch,list,buy){visited.add(n.id);// ซื้อยาก่อน แล้วอาวุธ/เกราะที่แพงสุดที่ซื้อได้
   for(let i=0;i<6;i++){const it=[...list].sort((a,b)=>(b.kind==="item"?0:1)-(a.kind==="item"?0:1)||b.price-a.price).find(x=>x.price<=ch.gas&&(x.kind!=="item"||x.id==="potion"));if(!it)break;if(buy(it))break;}},
 async battleMenu({P,E,pot,fire}){return E.boss&&E.charge===2?"guard":P.hp<P.maxhp*0.4&&pot>0?"potion":fire?"fire":P.mp>=4&&P.m_atk>P.p_atk?"bolt":"heavy";},
 async end(n,st,A,ch){ended++;stat.lv+=ch.level;stat.gas+=ch.gas;stat.long+=st.log.length;st.flags.forEach(f=>flags[f]=(flags[f]||0)+1);Object.entries(st.roots).forEach(([k,v])=>{const key=k+':'+v;flags[key]=(flags[key]||0)+1;});}
});
(async()=>{for(let i=0;i<N;i++){
  Object.keys(mem).forEach(k=>delete mem[k]);
  const c=Vault.create({name:"ทดสอบ",stats:{hp:130,p_atk:3,m_atk:2,p_def:2,m_def:2,spd:5,luck:1,wit:10,mana:20}});
  const k=Campaign.create("t","h","solo");Campaign.addMember(k,"h",Vault.checkout(c.cid,"t"));
  Story.setUI(pol());const g=await Story.start({data:D,campId:k.id});
  try{await Promise.race([g.run(),new Promise((_,rj)=>setTimeout(()=>rj(new Error("ค้าง/เวลาเกิน")),5000))]);}catch(e){errs.push(e.message);}
}
console.log(`เดินจบ ${ended}/${N} รอบ | เฉลี่ย Lv ${(stat.lv/ended).toFixed(1)} | กัส ${Math.round(stat.gas/ended)} | ตัดสินใจ★ ${(stat.long/ended).toFixed(1)} ครั้ง/รอบ`);
for(const f of['lost_to_goblins','lost_to_grak','lost_f2','lost_to_guardian','killed_guardian','guardian:calmed','guardian:fought','retreated_once','trap_safe','rescued_by_tib'])console.log(f.padEnd(22),String(Math.round(100*(flags[f]||0)/ended))+'%');
const all=Object.keys(D.act1.nodes);const un=all.filter(i=>!visited.has(i)&&["say","narr","choice","check","shop"].includes(D.act1.nodes[i].t));
console.log("โหนดที่ไม่เคยถูกเดินถึง:",un.length,un.slice(0,12).join(","));
if(errs.length){const c={};errs.forEach(e=>c[e]=(c[e]||0)+1);console.log("ERRORS",c);process.exit(1);}
})();
