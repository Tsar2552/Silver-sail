// กติกาต่อสู้ของโหมดเนื้อเรื่อง (ฟังก์ชันล้วน ทดสอบด้วย tools/sim_act1.js)
// ติด: d20 + ค่าเล็ง ≥ 10 + SPD เป้า | ดาเมจ: ((ATK+อาวุธ+ท่า)x3 − DEF x2) x (0.8+0.02 x d20) | ทอยได้ 20 = คริ x1.5 ติดเสมอ, 1 = พลาด
(function(g){
const MOVES={
  slash:{th:"ฟัน",power:6,kind:"p",mp:0,acc:0,info:"ท่าพื้นฐาน แม่น"},
  heavy:{th:"ฟันหนัก",power:12,kind:"p",mp:0,acc:-3,info:"แรงขึ้น แต่โอกาสติด −3"},
  bolt:{th:"ลูกเวท",power:9,kind:"m",mp:4,acc:0,info:"ใช้ M ATK และ MANA 4"},
};
const playerFrom=(c,inv)=>{const s=c.stats||{},wp=(c.weapon_power??1);return{
  name:c.name||"คุณ",hp:c.hp??s.hp??100,maxhp:s.hp??100,mp:c.mp??s.mana??20,maxmp:s.mana??20,
  p_atk:s.p_atk??3,m_atk:s.m_atk??2,p_def:s.p_def??2,m_def:s.m_def??2,spd:s.spd??5,luck:s.luck??1,wit:s.wit??10,wp,wstat:c.weapon_stat||"p",guard:false};};
const monsterFrom=(m,scale=1)=>({id:m[0],name:m[1],lv:m[3],hp:Math.round(m[4]*scale),maxhp:Math.round(m[4]*scale),atk:m[5],kind:m[6],p_def:m[7],m_def:m[8],spd:m[9],element:m[10],weak:m[11],boss:m[12],guard:false,charge:0});
const mult=d=>0.8+0.02*d;
function hit(rng,aim,tspd,bonus=0){const d=rng();const need=10+tspd;const tot=d+aim+bonus;
  return{d,tot,need,crit:d===20,ok:d===20||(d!==1&&tot>=need)};}
function dmg(rng,atk,wp,mp,def,crit,guard){const d=rng();let v=Math.floor(((atk+wp+mp)*3-def*2)*mult(d));v=Math.max(v,Math.ceil(atk*0.1),1);
  if(crit)v=Math.floor(v*1.5);if(guard)v=Math.floor(v/2);return{v,d};}
// ผู้เล่นโจมตี 1 ครั้ง -> คืนบรรทัดบันทึกพร้อมเหตุผล
function playerAttack(P,E,moveId,rng){const m=MOVES[moveId],L=[];
  if(m.mp>P.mp){L.push("MANA ไม่พอ ท่านี้ใช้ไม่ได้");return{L,used:false};}
  P.mp-=m.mp;const mg=m.kind==="m",aim=mg?Math.floor(P.wit/2):P.spd,h=hit(rng,aim,E.spd,m.acc);
  L.push(`🎲 d20=${h.d} + ค่าเล็ง ${aim}${m.acc?` ${m.acc}`:""} = ${h.tot} vs ${h.need} (10+SPD ${E.name} ${E.spd}) → ${h.crit?"คริติคอล!":h.ok?"โดน":"พลาด"}`);
  if(h.ok){const r=dmg(rng,mg?P.m_atk:P.p_atk,mg?0:P.wp,m.power,mg?E.m_def:E.p_def,h.crit,E.guard);E.hp=Math.max(0,E.hp-r.v);
    L.push(`⚔ ${P.name} ใช้${m.th}: ((${mg?P.m_atk:P.p_atk}+${mg?0:P.wp}+${m.power})x3 − DEF ${mg?E.m_def:E.p_def}x2) x ${mult(r.d).toFixed(2)} [d20=${r.d}] = ${r.v} ดาเมจ → ${E.name} HP ${E.hp}/${E.maxhp}`);}
  E.guard=false;return{L,used:true};}
// ศัตรูโจมตี: บอสสะสมพลัง 2 รอบแล้วโจมตีหนัก x1.5 (ประกาศล่วงหน้า ให้ผู้เล่นตั้งการ์ดทัน)
function enemyAttack(E,P,rng){const L=[];
  if(E.boss){E.charge++;if(E.charge===2){L.push(`⚠ ${E.name} เงื้ออาวุธสุดแรง! (รอบหน้าโจมตีหนัก x1.5 — ตั้งการ์ดได้)`);return L;}}
  const heavy=E.boss&&E.charge>=3;if(heavy)E.charge=0;
  const mg=E.kind==="m",h=hit(rng,E.spd,P.spd,0),def=mg?P.m_def:P.p_def;
  L.push(`🎲 ${E.name} d20=${h.d} + ${E.spd} = ${h.tot} vs ${h.need} (10+SPD คุณ ${P.spd}) → ${h.crit?"คริติคอล!":h.ok?"โดน":"พลาด"}`);
  if(h.ok){const r=dmg(rng,E.atk,0,0,def,h.crit,P.guard);let v=heavy?Math.floor(r.v*1.5):r.v;P.hp=Math.max(0,P.hp-v);
    L.push(`💥 ${E.name} ${heavy?"โจมตีหนัก":"โจมตี"}: (${E.atk}x3 − DEF ${def}x2) x ${mult(r.d).toFixed(2)} [d20=${r.d}]${P.guard?" ÷2 (ตั้งการ์ด)":""} = ${v} → HP คุณ ${P.hp}/${P.maxhp}`);}
  return L;}
function allyAttack(A,E,rng){const h=rng()<=14,L=[];if(!h){L.push(`${A.name} พลาด`);return L;}
  const d=rng();let v=Math.max(1,Math.floor(((A.atk+A.wp+A.mp)*3-E.p_def*2)*mult(d)));if(E.guard)v=Math.floor(v/2);E.hp=Math.max(0,E.hp-v);
  L.push(`🤝 ${A.name} ช่วยโจมตี ${v} ดาเมจ [d20=${d}] → ${E.name} HP ${E.hp}/${E.maxhp}`);return L;}
const expOf=m=>m.lv*30*(m.boss?5:1);
const expNeed=lv=>150*lv*lv;
g.Battle={MOVES,playerFrom,monsterFrom,playerAttack,enemyAttack,allyAttack,hit,dmg,expOf,expNeed};
if(typeof module!=="undefined")module.exports=g.Battle;
})(typeof window!=="undefined"?window:globalThis);
