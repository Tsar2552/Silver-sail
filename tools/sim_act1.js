// จำลองบอสด่าน Act 1 หลายพันรอบ เพื่อเช็กสมดุล: node tools/sim_act1.js
const B=require("../js/battle.js"),fs=require("fs");
const mon=Object.fromEntries(JSON.parse(fs.readFileSync(__dirname+"/../data/monsters.json","utf8")).monsters.map(m=>[m[0],m]));
const rng=()=>1+Math.floor(Math.random()*20);
function fight(P0,ids,{ally,potions=2,scale=1}){
  const P={...P0},Es=ids.map(i=>B.monsterFrom(mon[i],scale)),A=ally&&{...ally};let rounds=0;
  while(P.hp>0&&Es.some(e=>e.hp>0)&&rounds++<80){
    const E=Es.find(e=>e.hp>0);const lowHp=P.hp<P.maxhp*0.4;
    P.guard=false;
    if(E.boss&&E.charge===2){P.guard=true;}
    else if(lowHp&&potions>0){potions--;P.hp=Math.min(P.maxhp,P.hp+60);}
    else B.playerAttack(P,E,P.mp>=4&&P.m_atk>P.p_atk?"bolt":"heavy",rng);
    if(A&&E.hp>0)B.allyAttack(A,E,rng);
    Es.filter(e=>e.hp>0).forEach(e=>B.enemyAttack(e,P,rng));
  }
  return P.hp>0&&!Es.some(e=>e.hp>0);
}
const base={name:"ผู้กล้า",stats:{hp:130,p_atk:3,m_atk:2,p_def:2,m_def:2,spd:5,wit:10,mana:20,luck:1}};
const mk=(wp,hp)=>B.playerFrom({...base,weapon_power:wp,stats:{...base.stats,hp}});
const karel={name:"คาเรล",atk:4,wp:2,mp:3};
const N=3000,rate=(P,ids,o)=>{let w=0;for(let i=0;i<N;i++)w+=fight(P,ids,o);return Math.round(100*w/N);};
const rows=[
 ["ชั้น1 ก็อบลินสอดแนม x2 (ดาบเหล็ก, ไม่มียา)",mk(3,130),["goblin_scout","goblin_scout"],{potions:0}],
 ["ชั้น1 หนู+เมือก (มือเปล่า)",mk(1,130),["cave_rat","cave_slime"],{potions:0}],
 ["กรัก+คาเรล (ดาบเหล็ก, ยา 2)",mk(3,130),["grak"],{ally:karel,potions:2}],
 ["กรัก+คาเรล (ดาบเหล็ก, ยา 1)",mk(3,130),["grak"],{ally:karel,potions:1}],
 ["กรัก เดี่ยว (ดาบเหล็ก, ยา 3)",mk(3,130),["grak"],{potions:3}],
 ["กรัก+คาเรล+วางกับดักสำเร็จ (HP กรัก x0.7)",mk(3,130),["grak"],{ally:karel,potions:2,scale:0.7}],
 ["ชั้น2 งูเหล็ก (เหล็กกล้า Lv3 ยา 3)",mk(5,150),["iron_snake"],{potions:3}],
 ["ชั้น2 ก็อบลินนักขุด+หมอผี (เหล็กกล้า Lv3 ยา 3)",mk(5,150),["goblin_miner","goblin_shaman"],{potions:3}],
 ["ผู้พิทักษ์ เตรียมครบ 3 ข้อ (HP x0.35, ยา 4, คาเรล)",mk(7,170),["mine_guardian"],{ally:karel,potions:4,scale:0.35}],
 ["ผู้พิทักษ์ เตรียม 2 ข้อ (HP x0.5)",mk(7,170),["mine_guardian"],{ally:karel,potions:4,scale:0.5}],
 ["ผู้พิทักษ์ เตรียม 1 ข้อ (HP x0.7)",mk(7,170),["mine_guardian"],{ally:karel,potions:4,scale:0.7}],
 ["ผู้พิทักษ์ ไม่เตรียมเลย",mk(7,170),["mine_guardian"],{ally:karel,potions:4}],
];
rows.forEach(([n,P,ids,o])=>console.log(String(rate(P,ids,o)).padStart(3)+"%  "+n));
