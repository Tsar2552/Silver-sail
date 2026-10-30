// เอนจินเนื้อเรื่องสไตล์ RPG ยุคเก่า: กล่องข้อความ, 3 ตัวเลือก, ทอย d20 เมื่อกดตกลง, ต่อสู้ผลัดตา
const Story=(()=>{
const DEF={hp:130,p_atk:3,m_atk:2,p_def:2,m_def:2,spd:5,luck:1,wit:10,mana:20};
let A,D,camp,ch,st,rng=()=>1+Math.floor(Math.random()*20),ui;
const want=(c)=>{if(!c)return false;if(c.includes(":")){const[k,v]=c.split(":");return st.roots[k]===v;}return st.flags.includes(c);};
const itemOf=id=>D.items.items.find(i=>i.id===id);
const wpn=id=>D.weapons.weapons.find(w=>w.id===id),arm=id=>D.armor.armor.find(a=>a.id===id);
function stats(){const b={...DEF,...(ch.stats||{})},lv=ch.level||1,e=ch.equip||{},a=e.armor&&arm(e.armor);
  const s={...b,hp:b.hp+(lv-1)*10+(a?a.hp:0),mana:b.mana+(lv-1)*2,p_def:b.p_def+(a?a.p_def:0),m_def:b.m_def+(a?a.m_def:0),spd:b.spd+(a?a.spd:0)};
  const w=e.weapon&&wpn(e.weapon);s.wp=w?w.power:1;s.wstat=w?w.stat:"p";s.welem=w?w.element:null;return s;}
function save(){if(!camp)return;camp.flags=st.flags;camp.roots=st.roots;camp.story={node:st.node,act:1};camp.party[0].char=ch;Campaign.put(camp);}
function inv(id,n){ch.inv=Array.isArray(ch.inv)?{}:ch.inv||{};if(n)ch.inv[id]=Math.max(0,(ch.inv[id]||0)+n);return ch.inv[id]||0;}
function gain(exp){ch.exp=(ch.exp||0)+exp;ch.level=ch.level||1;const up=[];
  while(ch.exp>=Battle.expNeed(ch.level)){ch.exp-=Battle.expNeed(ch.level);ch.level++;up.push(ch.level);}return up;}
function heal(full){const s=stats();ch.hp=full?s.hp:Math.min(s.hp,(ch.hp??s.hp));ch.mp=full?s.mana:(ch.mp??s.mana);}
function apply(d,out){if(!d)return;
  if(d.gasmin&&(ch.gas||0)<d.gasmin)ch.gas=d.gasmin;
  for(const k of["gas","gasplus"])if(d[k]){ch.gas=Math.max(0,(ch.gas||0)+d[k]);out.push(`${d[k]>0?"+":""}${d[k]} กัส`);}
  if(d.exp){const up=gain(d.exp);out.push(`+${d.exp} EXP`);up.forEach(l=>{out.push(`⬆ เลเวลอัป! Lv ${l} (HP +10, MANA +2)`);});}
  if(d.item)for(const[k,n]of Object.entries(d.item)){if(n)out.push(`${n>0?"ได้":"เสีย"} ${itemOf(k).th} x${Math.abs(n)}`);inv(k,n);}
  if(d.flag)d.flag.forEach(f=>{if(!st.flags.includes(f))st.flags.push(f);});
  if(d.root)Object.assign(st.roots,d.root);
  if(d.hp){ch.hp=Math.max(1,(ch.hp??stats().hp)+d.hp);out.push(`${d.hp} HP`);}
  if(d.heal){heal(true);out.push("HP/MANA ฟื้นเต็ม");}
  if(d.ally)st.ally=d.ally;}
const lines=[];
async function run(id){
  while(true){const n=A.nodes[id];if(!n)throw new Error("ไม่พบโหนด "+id);st.node=id;
    if(n.bg){st.bg=n.bg;ui.bg(st.bg);}
    const out=[];apply(n.do,out);ui.status(ch,stats());if(out.length)ui.toast(out);
    if(n.t==="say"||n.t==="narr"){await ui.say(n);save();id=n.next;continue;}
    if(n.t==="jump"){const hit=(n.cases||[]).find(c=>want(c[0]));id=hit?hit[1]:n.next;continue;}
    if(n.t==="choice"){save();const i=await ui.choice(n);const o=n.opts[i];const o2=[];apply(o.do,o2);
      if(o.long)st.log.push({node:id,prompt:n.prompt,pick:o.text,note:o.note||""});
      ui.status(ch,stats());if(o2.length)ui.toast(o2);save();id=o.goto;continue;}
    if(n.t==="check"){const s=stats(),val=s[n.stat]??0;const r=await ui.check(n,val,rng);id=r?n.ok:n.fail;if(r!==undefined)apply({},[]);save();continue;}
    if(n.t==="shop"){await ui.shop(n,ch,shopList(n),(it,price)=>buy(it,price));save();id=n.next;continue;}
    if(n.t==="battle"){const res=await fight(n);save();id=res==="win"?n.win:n.lose;continue;}
    if(n.t==="end"){await ui.end(n,st,A,ch);return;}
    throw new Error("ชนิดโหนดไม่รู้จัก "+n.t);}}
function shopList(n){return n.items.map(i=>{if(i[0]==="@"){const it=itemOf(i.slice(1));return{id:it.id,th:it.th,price:it.price,desc:it.desc,kind:"item"};}
  const w=wpn(i);if(w)return{id:w.id,th:w.th,price:w.price,desc:`${w.type_th} พลัง ${w.power} · ${w.hands} มือ`+(w.element?` · ธาตุ${w.element}`:""),kind:"weapon"};
  const a=arm(i);return{id:a.id,th:a.th,price:a.price,desc:`${a.type_th} P.DEF +${a.p_def} M.DEF +${a.m_def}${a.hp?` HP +${a.hp}`:""}`,kind:"armor"};});}
function buy(it){if((ch.gas||0)<it.price)return"กัสไม่พอ";ch.gas-=it.price;
  if(it.kind==="item")inv(it.id,1);
  else{ch.equip=ch.equip||{};ch.equip[it.kind]=it.id;heal(false);}
  ui.status(ch,stats());save();return null;}
const PREP={grak:[1,.85,.7,.6],mine_guardian:[1,.7,.5,.35]};
async function fight(n){
  const mon=Object.fromEntries(D.monsters.monsters.map(m=>[m[0],m]));
  const cnt=(n.prep||[]).filter(f=>want(f)).length;
  const Es=n.enemies.map(i=>{const sc=(PREP[i]||[1,1,1,1])[cnt];return Battle.monsterFrom(mon[i],sc);});
  const s=stats();const P=Battle.playerFrom({name:ch.name,stats:s,weapon_power:s.wp,hp:ch.hp??s.hp,mp:ch.mp??s.mana});
  const ally=n.ally&&want("ally_"+n.ally)?{name:"คาเรล",atk:4,wp:2,mp:3}:null;
  const hasFire=()=>inv("fireflask")>0,pot=()=>inv("potion");
  ui.battleStart(n,Es,cnt,!!ally);let round=0;
  while(P.hp>0&&Es.some(e=>e.hp>0)){
    round++;const E=Es.find(e=>e.hp>0);P.guard=false;
    const act=await ui.battleMenu({P,Es,E,round,pot:pot(),fire:hasFire(),spells:P.mp>=4,flee:n.flee!==false});
    const L=[];
    if(act==="guard"){P.guard=true;L.push("🛡 ตั้งการ์ด: ดาเมจที่รับรอบนี้ลดครึ่ง");}
    else if(act==="potion"){inv("potion",-1);P.hp=Math.min(P.maxhp,P.hp+60);L.push(`🧪 ใช้ยาฟื้นฟู +60 HP → ${P.hp}/${P.maxhp}`);}
    else if(act==="fire"){inv("fireflask",-1);const known=want("known_weak_fire")&&E.weak==="fire";const v=known?100:50;E.hp=Math.max(0,E.hp-v);
      L.push(`🔥 ขว้างขวดไฟ: 50${known?" x2 (รู้ว่ากลัวไฟ)":""} = ${v} ดาเมจ → ${E.name} HP ${E.hp}/${E.maxhp}`);}
    else if(act==="flee"){const d=rng(),t=d+P.spd;L.push(`🎲 หนี: d20=${d} + SPD ${P.spd} = ${t} vs 12 → ${t>=12?"หนีสำเร็จ":"หนีไม่พ้น"}`);
      if(t>=12){ui.battleLog(L);ch.hp=P.hp;ch.mp=P.mp;ui.battleEnd();return"lose";}}
    else{const r=Battle.playerAttack(P,E,act,rng);L.push(...r.L);}
    if(ally&&E.hp>0)L.push(...Battle.allyAttack(ally,E,rng));
    if(Es.every(e=>e.hp<=0)){ui.battleLog(L);break;}
    Es.filter(e=>e.hp>0).forEach(e=>{L.push(...Battle.enemyAttack(e,P,rng));});
    ui.battleLog(L);ui.battleRefresh(P,Es);
  }
  const win=P.hp>0;ch.hp=win?P.hp:stats().hp;ch.mp=P.mp;ui.battleEnd();
  if(win){const out=[];const exp=Es.reduce((a,e)=>a+Battle.expOf(e),0);
    const gas=Es.reduce((a,e)=>a+e.lv*8*(e.boss?4:1),0);apply({exp,gasplus:gas},out);ui.toast(["ชนะ!",...out]);}
  ui.status(ch,stats());return win?"win":"lose";}
async function start({data,campId,debug}){D=data;A=D.act1;
  camp=campId?Campaign.get(campId):null;
  const dflt={cid:"demo",name:"ผู้กล้า",level:1,exp:0,gas:0,inv:{},stats:{}};
  ch=camp?camp.party[0].char:dflt;ch.inv=Array.isArray(ch.inv)?{}:ch.inv||{};
  st={flags:camp?camp.flags:[],roots:camp?camp.roots:{},node:A.start,bg:null,ally:null,log:[]};
  if(camp&&camp.story&&camp.story.node&&A.nodes[camp.story.node])st.node=camp.story.node;
  if(ch.hp==null)heal(true);
  return {run:()=>run(st.node),getState:()=>({st,ch,camp})};}
return{start,want:c=>want(c),setUI:u=>{ui=u;},rngSet:f=>{rng=f;}};
})();
if(typeof module!=="undefined")module.exports=Story;
