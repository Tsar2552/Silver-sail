// ทดสอบตรรกะเซฟ: node tools/test_vault.js
const mem={};globalThis.localStorage={getItem:k=>mem[k]??null,setItem:(k,v)=>{mem[k]=v}};
const {Vault,Campaign}=require("../js/vault.js");const A=require("assert");
const c=Vault.create({name:"เอ"});
const copy=Vault.checkout(c.cid,"1234");A.ok(Vault.get(c.cid).lock,"ล็อกหลังเช็กเอาต์");
copy.level=3;copy.gas=500;
A.deepStrictEqual(Vault.checkin(copy,"act1"),{ok:true});
let v=Vault.get(c.cid);A.strictEqual(v.rev,2);A.strictEqual(v.level,3);A.strictEqual(v.lock,null);A.strictEqual(v.history.length,1);
// ชนกัน: สองห้องเช็กเอาต์พร้อมกัน
const x=Vault.checkout(c.cid,"1111"),y=Vault.checkout(c.cid,"2222");x.gas=1;y.gas=2;
A.ok(Vault.checkin(x).ok);const r=Vault.checkin(y);A.ok(r.conflict);A.strictEqual(Vault.all().length,2,"ไม่ทำของหาย");
// เนื้อเรื่อง
const k=Campaign.create("ทดสอบ","โฮสต์");Campaign.addMember(k,"เอ",Vault.checkout(c.cid,"3333"));
for(let i=0;i<7;i++)Campaign.snapshot(k,"s"+i);A.strictEqual(k.backups.length,5);
const out=Campaign.finishAct(k);A.strictEqual(k.act,2);A.strictEqual(out.length,1);
k.party[0].char.gas=999;A.ok(Campaign.restore(k,0));A.notStrictEqual(k.party[0].char.gas,999);
console.log("ผ่านทั้งหมด");
