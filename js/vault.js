// ระบบเซฟ 2 ชั้น (ดู docs/SAVE_SPEC.md)
//  - Vault   : คลังตัวละครส่วนตัว (อยู่ในเบราว์เซอร์ผู้เล่น)
//  - Campaign: เซฟเนื้อเรื่อง/ปาร์ตี้ (อยู่ที่ Host; เล่นคนเดียว = Host คือตัวเอง)
// ตัวละครเข้าเนื้อเรื่อง = "เช็กเอาต์สำเนา" และกลับคลังตอนจบ act = "เช็กอิน" (ตรวจ rev กันทับกัน)
(function(g){
const rnd=()=>Math.random().toString(36).slice(2,8);
const store=()=>g.localStorage;
const rd=(k,d)=>{try{return JSON.parse(store().getItem(k))??d}catch(e){return d}};
const wr=(k,v)=>{try{store().setItem(k,JSON.stringify(v));return true}catch(e){return false}};
const VK="ssail_vault_v1",CK="ssail_campaigns_v1";
const Vault={
  all:()=>rd(VK,[]),
  get:cid=>Vault.all().find(c=>c.cid===cid),
  put(c){const l=Vault.all().filter(x=>x.cid!==c.cid);return wr(VK,[{...c,updated:Date.now()},...l]);},
  create({name,slots,stats}){const c={cid:"c"+Date.now().toString(36)+rnd(),rev:1,name:name||"ไร้นาม",slots:slots||{},stats:stats||{},level:1,exp:0,gas:0,inv:[],flags:[],history:[],lock:null,created:Date.now()};Vault.put(c);return c;},
  remove:cid=>wr(VK,Vault.all().filter(c=>c.cid!==cid)),
  // เช็กเอาต์: ได้สำเนาไปเล่น + ล็อกอ่อนในคลัง (เตือนถ้านำไปเข้าห้องอื่น)
  checkout(cid,room){const c=Vault.get(cid);if(!c)return null;Vault.put({...c,lock:{room,since:Date.now()}});return{...c,baseRev:c.rev,lock:null};},
  // เช็กอิน: rev ตรง -> ทับและ rev+1 ; ไม่ตรง -> เก็บเป็นสำเนาแยก (ไม่ทำของหาย)
  checkin(copy,note){const cur=Vault.get(copy.cid),{baseRev,...rest}=copy;
    if(!cur){Vault.put({...rest,rev:1,lock:null});return{ok:true,created:true};}
    if(cur.rev!==baseRev){const alt={...rest,cid:cur.cid+"-b"+rnd(),name:cur.name+" (สำเนาชนกัน)",rev:1,lock:null};Vault.put(alt);Vault.put({...cur,lock:null});return{ok:false,conflict:true,altCid:alt.cid};}
    Vault.put({...rest,rev:cur.rev+1,lock:null,history:[...(rest.history||[]),{t:Date.now(),note:note||"จบ act"}]});return{ok:true};},
  unlock(cid){const c=Vault.get(cid);if(c)Vault.put({...c,lock:null});}
};
const Campaign={
  all:()=>rd(CK,[]),
  get:id=>Campaign.all().find(c=>c.id===id),
  put(c){const l=Campaign.all().filter(x=>x.id!==c.id);return wr(CK,[{...c,updated:Date.now()},...l]);},
  create(title,host,kind){const c={id:"k"+Date.now().toString(36)+rnd(),kind:kind||"multi",title:title||"การผจญภัยใหม่",host,act:1,chapter:0,flags:[],roots:{},party:[],log:[],backups:[],created:Date.now()};Campaign.put(c);return c;},
  addMember(camp,owner,copy){camp.party=camp.party.filter(m=>m.char.cid!==copy.cid).concat([{owner,char:copy}]);Campaign.put(camp);return camp;},
  // สแนปช็อตกลิ้ง 5 ชุด (เรียกตอนจบฉาก/จบ act)
  snapshot(camp,label){const snap={t:Date.now(),label:label||"auto",act:camp.act,chapter:camp.chapter,party:JSON.parse(JSON.stringify(camp.party)),flags:[...camp.flags],roots:{...camp.roots}};
    camp.backups=[snap,...camp.backups].slice(0,5);Campaign.put(camp);return snap;},
  restore(camp,i){const s=camp.backups[i];if(!s)return false;Object.assign(camp,{act:s.act,chapter:s.chapter,party:s.party,flags:s.flags,roots:s.roots});Campaign.put(camp);return true;},
  // ปิด act: ขยับ act และคืนรายการ {owner,char} ให้ส่งกลับผู้เล่น
  finishAct(camp,note){Campaign.snapshot(camp,"จบ act "+camp.act);const out=camp.party.map(m=>({owner:m.owner,char:{...m.char}}));camp.act++;camp.chapter=0;Campaign.put(camp);return out;},
  // ลบเซฟ: ปลดล็อกตัวละครของสมาชิกที่ล็อกกับเซฟนี้ในคลังเครื่องนี้
  remove(id){const k=Campaign.get(id);if(k)k.party.forEach(m=>{const c=Vault.get(m.char.cid);if(c&&c.lock)Vault.unlock(c.cid);});wr(CK,Campaign.all().filter(c=>c.id!==id));}
};
g.Vault=Vault;g.Campaign=Campaign;
if(typeof module!=="undefined")module.exports={Vault,Campaign};
})(typeof window!=="undefined"?window:globalThis);
