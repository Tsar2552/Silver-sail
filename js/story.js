// เอนจินเนื้อเรื่อง (รองรับปาร์ตี้ 1–4 คน): เล่นคนเดียว = ปาร์ตี้ 1 คน
// ui ต้องมี: bg status toast say choice check shop battleStart battleActions battleLog battleRefresh battleEnd end
const Story=(()=>{
const DEF={hp:130,p_atk:3,m_atk:2,p_def:2,m_def:2,spd:5,luck:1,wit:10,mana:20};
const HPF=[1,2.0,3.1,4.4];            // ตัวคูณ HP ศัตรูตามจำนวนผู้เล่น
let A,D,camp,party,owners,st,rng=()=>1+Math.floor(Math.random()*20),ui;
const want=c=>{if(!c)return false;if(c.includes(":")){const[k,v]=c.split(":");return st.roots[k]===v;}return st.flags.includes(c);};
const itemOf=id=>D.items.items.find(i=>i.id===id);
const wpn=id=>D.weapons.weapons.find(w=>w.id===id),arm=id=>D.armor.armor.find(a=>a.id===id);
function stats(ch){const b={...DEF,...(ch.stats||{})},lv=ch.level||1,e=ch.equip||{},a=e.armor&&arm(e.armor);
  const s={...b,hp:b.hp+(lv-1)*10+(a?a.hp:0),mana:b.mana+(lv-1)*2,p_def:b.p_def+(a?a.p_def:0),m_def:b.m_def+(a?a.m_def:0),spd:b.spd+(a?a.spd:0)};
  const w=e.weapon&&wpn(e.weapon);s.wp=w?w.power:1;s.wstat=w?w.stat:"p";return s;}
function save(){if(!camp)return;camp.flags=st.flags;camp.roots=st.roots;camp.story={node:st.node,act:camp.act};camp.party.forEach((m,i)=>{m.char=party[i];});Campaign.put(camp);}
function inv(ch,id,n){ch.inv=Array.isArray(ch.inv)?{}:ch.inv||{};if(n)ch.inv[id]=Math.max(0,(ch.inv[id]||0)+n);return ch.inv[id]||0;}
function gain(ch,exp){ch.exp=(ch.exp||0)+exp;ch.level=ch.level||1;const up=[];while(ch.exp>=Battle.expNeed(ch.level)){ch.exp-=Battle.expNeed(ch.level);ch.level++;up.push(ch.level);}return up;}
function heal(ch,full){const s=stats(ch);ch.hp=full?s.hp:Math.min(s.hp,(ch.hp??s.hp));ch.mp=full?s.mana:(ch.mp??s.mana);}
function apply(d,out){if(!d)return;
  party.forEach((ch,pi)=>{const o=pi===0?out:[];
    if(d.gasmin&&(ch.gas||0)<d.gasmin)ch.gas=d.gasmin;
    for(const k of["gas","gasplus"])if(d[k]){ch.gas=Math.max(0,(ch.gas||0)+d[k]);o.push(`${d[k]>0?"+":""}${d[k]} กัส`);}
    if(d.exp){const up=gain(ch,d.exp);o.push(`+${d.exp} EXP`);up.forEach(l=>o.push(`⬆ ${ch.name} เลเวลอัป! Lv ${l}`));}
    if(d.item)for(const[k,n]of Object.entries(d.item)){if(n)o.push(`${n>0?"ได้":"เสีย"} ${itemOf(k).th} x${Math.abs(n)}`);inv(ch,k,n);}
    if(d.hp){ch.hp=Math.max(1,(ch.hp??stats(ch).hp)+d.hp);o.push(`${d.hp} HP`);}
    if(d.heal){heal(ch,true);o.push("HP/MANA ฟื้นเต็ม");}});
  if(d.flag)d.flag.forEach(f=>{if(!st.flags.includes(f))st.flags.push(f);});
  if(d.root)Object.assign(st.roots,d.root);}
const pub=()=>party.map((c,i)=>({name:c.name,owner:owners[i],level:c.level||1,hp:c.hp??stats(c).hp,maxhp:stats(c).hp,mp:c.mp??stats(c).mana,maxmp:stats(c).mana,gas:c.gas||0}));
const refresh=()=>ui.status(pub());
async function run(id){
  while(true){const n=A.nodes[id];if(!n)throw new Error("ไม่พบโหนด "+id);st.node=id;
    if(n.bg){st.bg=n.bg;ui.bg(st.bg);}
    const out=[];apply(n.do,out);refresh();if(out.length)ui.toast(out);
    if(n.t==="say"||n.t==="narr"){await ui.say(n);save();id=n.next;continue;}
    if(n.t==="jump"){const hit=(n.cases||[]).find(c=>want(c[0]));id=hit?hit[1]:n.next;continue;}
    if(n.t==="choice"){save();const i=await ui.choice(n);const o=n.opts[i];const o2=[];apply(o.do,o2);
      if(o.long)st.log.push({node:id,prompt:n.prompt,pick:o.text,note:o.note||""});
      refresh();if(o2.length)ui.toast(o2);save();id=o.goto;continue;}
    if(n.t==="check"){const ok=await ui.check(n,party.map(c=>stats(c)[n.stat]??0),rng);save();id=ok?n.ok:n.fail;continue;}
    if(n.t==="shop"){await ui.shop(n,party,pi=>shopList(n),(pi,it)=>buy(pi,it));save();id=n.next;continue;}
    if(n.t==="battle"){const res=await fight(n);save();id=res==="win"?n.win:n.lose;continue;}
    if(n.t==="end"){await ui.end(n,st,A,party);return;}
    throw new Error("ชนิดโหนดไม่รู้จัก "+n.t);}}
function shopList(n){return n.items.map(i=>{if(i[0]==="@"){const it=itemOf(i.slice(1));return{id:it.id,th:it.th,price:it.price,desc:it.desc,kind:"item"};}
  const w=wpn(i);if(w)return{id:w.id,th:w.th,price:w.price,desc:`${w.type_th} พลัง ${w.power} · ${w.hands} มือ`+(w.element?` · ธาตุ${w.element}`:""),kind:"weapon"};
  const a=arm(i);return{id:a.id,th:a.th,price:a.price,desc:`${a.type_th} P.DEF +${a.p_def} M.DEF +${a.m_def}${a.hp?` HP +${a.hp}`:""}`,kind:"armor"};});}
function buy(pi,it){const ch=party[pi];if(!ch||!it)return"ซื้อไม่ได้";if((ch.gas||0)<it.price)return"กัสไม่พอ";ch.gas-=it.price;
  if(it.kind==="item")inv(ch,it.id,1);else{ch.equip=ch.equip||{};ch.equip[it.kind]=it.id;heal(ch,false);}
  refresh();save();return null;}
const PREP={grak:[1,.85,.7,.6],mine_guardian:[1,.7,.5,.35]};
async function fight(n){
  const mon=Object.fromEntries(D.monsters.monsters.map(m=>[m[0],m]));const N=party.length;
  const cnt=(n.prep||[]).filter(f=>want(f)).length;
  const Es=n.enemies.map(i=>Battle.monsterFrom(mon[i],(PREP[i]||[1,1,1,1])[cnt]*HPF[N-1]));
  const Ps=party.map(ch=>{const s=stats(ch);return Battle.playerFrom({name:ch.name,stats:s,weapon_power:s.wp,hp:ch.hp??s.hp,mp:ch.mp??s.mana});});
  const ally=N===1&&n.ally&&want("ally_"+n.ally)?{name:"คาเรล",atk:4,wp:2,mp:3}:null;
  ui.battleStart(n,Es,cnt,!!ally,Ps);let round=0,fled=false;
  const alive=()=>Ps.some(p=>p.hp>0),foes=()=>Es.some(e=>e.hp>0);
  while(alive()&&foes()&&!fled){
    round++;Ps.forEach(p=>p.guard=false);
    const invs=party.map(c=>({pot:inv(c,"potion"),fire:inv(c,"fireflask")}));
    const acts=await ui.battleActions({Ps,Es,round,invs,flee:n.flee!==false});
    const L=[];const order=Ps.map((p,i)=>i).filter(i=>Ps[i].hp>0).sort((a,b)=>Ps[b].spd-Ps[a].spd);
    for(const i of order){const P=Ps[i],E=Es.find(e=>e.hp>0);if(!E)break;const act=acts[i]||"heavy",ch=party[i];
      if(act==="guard"){P.guard=true;L.push(`🛡 ${P.name} ตั้งการ์ด: ดาเมจที่รับรอบนี้ลดครึ่ง`);}
      else if(act==="potion"&&inv(ch,"potion")>0){inv(ch,"potion",-1);P.hp=Math.min(P.maxhp,P.hp+60);L.push(`🧪 ${P.name} ใช้ยาฟื้นฟู +60 HP → ${P.hp}/${P.maxhp}`);}
      else if(act==="fire"&&inv(ch,"fireflask")>0){inv(ch,"fireflask",-1);const known=want("known_weak_fire")&&E.weak==="fire";const v=known?100:50;E.hp=Math.max(0,E.hp-v);
        L.push(`🔥 ${P.name} ขว้างขวดไฟ: 50${known?" x2 (รู้ว่ากลัวไฟ)":""} = ${v} ดาเมจ → ${E.name} HP ${E.hp}/${E.maxhp}`);}
      else if(act==="flee"){const d=rng(),t=d+P.spd;L.push(`🎲 ${P.name} พาหนี: d20=${d} + SPD ${P.spd} = ${t} vs 12 → ${t>=12?"หนีสำเร็จ":"หนีไม่พ้น"}`);if(t>=12){fled=true;break;}}
      else if(["slash","heavy","bolt"].includes(act)){const r=Battle.playerAttack(P,E,act,rng);L.push(...r.L);}
    }
    if(fled){ui.battleLog(L);break;}
    if(ally&&foes())L.push(...Battle.allyAttack(ally,Es.find(e=>e.hp>0),rng));
    if(foes())Es.filter(e=>e.hp>0).forEach(e=>{const al=Ps.filter(p=>p.hp>0);if(!al.length)return;L.push(...Battle.enemyAttack(e,al[(rng()-1)%al.length],rng));});
    ui.battleLog(L);ui.battleRefresh(Ps,Es);
  }
  const win=!fled&&alive()&&!foes();
  Ps.forEach((p,i)=>{const s=stats(party[i]);party[i].hp=win?(p.hp>0?p.hp:Math.ceil(s.hp*.3)):s.hp;party[i].mp=p.mp;});
  ui.battleEnd();
  if(win){const out=[];const exp=Es.reduce((a,e)=>a+Battle.expOf(e),0),gas=Es.reduce((a,e)=>a+e.lv*8*(e.boss?4:1),0);apply({exp,gasplus:gas},out);ui.toast(["ชนะ!",...out]);}
  refresh();return win?"win":"lose";}
async function start({data,campId,chars}){D=data;A=data.act||data.act1;
  camp=campId?Campaign.get(campId):null;
  if(camp){party=camp.party.map(m=>m.char);owners=camp.party.map(m=>m.owner);st={flags:camp.flags,roots:camp.roots,node:A.start,bg:null,log:camp.storyLog||[]};
    if(camp.story&&camp.story.node&&A.nodes[camp.story.node])st.node=camp.story.node;}
  else{party=chars||[{cid:"demo",name:"ผู้กล้า",level:1,exp:0,gas:0,inv:{},stats:{}}];owners=party.map(c=>c.name);st={flags:[],roots:{},node:A.start,bg:null,log:[]};}
  party.forEach(c=>{c.inv=Array.isArray(c.inv)?{}:c.inv||{};if(c.hp==null)heal(c,true);});
  return{run:()=>run(st.node),getState:()=>({st,party,camp,owners}),pub};}
return{start,want:c=>want(c),setUI:u=>{ui=u;},rngSet:f=>{rng=f;},stats};
})();
if(typeof module!=="undefined")module.exports=Story;
