// ตัวช่วยร่วม: โหลดข้อมูล, เซฟ (localStorage + ไฟล์ JSON)
const $=(q,r=document)=>r.querySelector(q),$$=(q,r=document)=>[...r.querySelectorAll(q)];
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const loadData=async names=>Object.fromEntries(await Promise.all(names.map(async n=>[n,await (await fetch(`data/${n}.json`)).json()])));
const Saves={
  key:"ssail_saves_v1",
  all(){try{return JSON.parse(localStorage.getItem(this.key)||"[]")}catch(e){return[]}},
  put(list){try{localStorage.setItem(this.key,JSON.stringify(list))}catch(e){alert("บันทึกในเบราว์เซอร์ไม่ได้ (โหมดส่วนตัว?) ใช้ปุ่มส่งออกไฟล์แทน")}},
  create(name,mode="solo"){const s={id:"s"+Date.now().toString(36),name:name||"เซฟใหม่",mode,created:Date.now(),updated:Date.now(),state:{notes:"",flags:[]}};this.put([s,...this.all()]);return s;},
  get(id){return this.all().find(s=>s.id===id)},
  update(id,state){const l=this.all().map(s=>s.id===id?{...s,state,updated:Date.now()}:s);this.put(l);},
  remove(id){this.put(this.all().filter(s=>s.id!==id))},
  exportFile(s){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(s,null,1)],{type:"application/json"}));a.download=`silversail_${s.name}_${s.id}.json`;a.click();},
  importFile(file){return file.text().then(t=>{const s=JSON.parse(t);if(!s.id||!s.state)throw new Error("ไฟล์เซฟไม่ถูกต้อง");this.put([s,...this.all().filter(x=>x.id!==s.id)]);return s;});}
};
