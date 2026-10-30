// เล่นหลายคน: Host รันเอนจิน, ทุกคน "โหวต" ตัวเลือก, ทอยเช็กร่วม, ต่อสู้เลือกท่าพร้อมกัน
// ไม่แตะ DOM/เครือข่ายโดยตรง: รับ V (หน้าจอ) และ T (ตัวส่งข้อความ) เข้ามา เพื่อทดสอบด้วย node ได้
//   T(host): broadcast(msg) send(owner,msg) onMsg(fn(owner,msg)) onLeave(fn(owner)) owners()
//   T(client): send(msg) onMsg(fn(msg))
(function(g){
const sleep=ms=>ms>0?new Promise(r=>setTimeout(r,ms)):Promise.resolve();

// ---------- เล่นคนเดียว ----------
function makeSPUI(V,{rng}){
  return{
    bg:V.bg,status:V.status,toast:V.toast,
    say:n=>V.say(n,{wait:true}),
    choice:n=>new Promise(res=>{V.choice(n,{canVote:true,canClose:false,onPick:i=>res(i)});}),
    async check(n,vals){const d={ok:false};await new Promise(res=>{V.check(n,[{owner:"",val:vals[0]}],{canRoll:true,onConfirm:res});});
      const r=rng(),val=vals[0],tot=r+val,ok=r===20||(r!==1&&tot>=n.dc);await V.checkResult(n,[{owner:"",d:r,val,tot,ok}],ok,{wait:true});return ok;},
    shop:(n,party,listOf,buy)=>new Promise(res=>{const h=V.shop(n.title||"ร้านค้า",listOf(0),{gas:()=>party[0].gas||0,canShop:true,canForce:true,onBuy:id=>{const it=listOf(0).find(x=>x.id===id);const e=buy(0,it);h.update();return e;},onDone:()=>{h.close();res();}});}),
    battleStart:(...a)=>V.battleStart(...a),battleLog:l=>V.battleLog(l),battleRefresh:(P,E)=>V.battleRefresh(P,E),battleEnd:()=>V.battleEnd(),
    battleActions:({Ps,Es,round,invs,flee})=>new Promise(res=>{V.battleMenu({Ps,Es,round,inv:invs[0],idx:0,flee},{onAct:a=>res([a])});}),
    end:(n,st,A,party)=>V.end(n,{log:st.log,party:party.map(c=>({name:c.name,level:c.level,gas:c.gas}))},{isHost:true,onFinish:null})
  };
}

// ---------- Host ----------
function makeHostUI(V,T,{hostName,rng,delay=1600,getState}){
  let cur={},last={bg:null,status:null,int:null};
  const owners=()=>getState().owners;
  const connected=()=>new Set([...T.owners(),hostName]);
  const voters=()=>[...new Set(owners().filter(o=>connected().has(o)))];
  const hostIn=()=>owners().includes(hostName);
  const bc=m=>T.broadcast(m);
  T.onMsg((o,m)=>{const f=cur[m.t];if(f)f(o,m);});
  T.onLeave(o=>{if(cur.leave)cur.leave(o);});
  const gather=(setup)=>new Promise(res=>setup(res));
  const ui={
    last,
    syncFor(owner){const out=[];if(last.bg)out.push({t:"bg",id:last.bg});if(last.status)out.push({t:"status",list:last.status});if(last.int)out.push(last.int);return out;},
    bg(id){last.bg=id;V.bg(id);bc({t:"bg",id});},
    status(list){last.status=list;V.status(list);bc({t:"status",list});},
    toast(arr){V.toast(arr);bc({t:"toast",arr});},
    async say(n){const m={t:"say",n:{sp:n.sp,emo:n.emo,text:n.text}};last.int=m;bc(m);await V.say(n,{wait:true});last.int=null;},
    async choice(n){
      const votes={};const msg={t:"choice",id:n.id,prompt:n.prompt,opts:n.opts.map(o=>({text:o.text,long:!!o.long})),voters:voters()};last.int=msg;bc(msg);
      const pick=await gather(res=>{
        let fin=false;const vs=()=>voters();
        const h=V.choice(n,{canVote:hostIn(),canClose:true,onPick:i=>cast(hostName,i),onClose:()=>finish()});
        const update=()=>{const voted=Object.keys(votes);bc({t:"tally",id:n.id,voted,total:vs()});h.tally(voted,vs());};
        const cast=(o,i)=>{if(fin||!vs().includes(o)||votes[o]!==undefined||i<0||i>=n.opts.length)return;votes[o]=i;if(o===hostName)h.lock("ส่งโหวตแล้ว");update();if(vs().every(x=>votes[x]!==undefined))finish();};
        const finish=()=>{if(fin||!Object.keys(votes).length)return;fin=true;
          const counts=n.opts.map((_,i)=>Object.values(votes).filter(v=>v===i).length),mx=Math.max(...counts),tied=counts.map((c,i)=>c===mx?i:-1).filter(i=>i>=0);
          let how="เสียงข้างมาก",p=tied[0];if(tied.length>1){const d=rng();p=tied[(d-1)%tied.length];how=`เสมอ → ทอย d20 = ${d} ตัดสินให้ข้อ ${p+1}`;}
          const text=`โหวต: ${counts.map((c,i)=>`ข้อ ${i+1} = ${c}`).join(" · ")} → ${how}`;
          bc({t:"result",id:n.id,counts,pick:p,text,votes});h.result(text,p);sleep(delay).then(()=>res(p));};
        cur={vote:(o,m)=>cast(o,m.i),leave:()=>{if(Object.keys(votes).length&&vs().every(x=>votes[x]!==undefined))finish();}};
        update();});
      cur={};last.int=null;return pick;},
    async check(n,vals){
      const vs=voters();const rows=owners().map((o,i)=>({owner:o,val:vals[i]})).filter(r=>vs.includes(r.owner));
      const msg={t:"check",n:{why:n.why,stat:n.stat,dc:n.dc},vals:rows,voters:vs};last.int=msg;bc(msg);
      await gather(res=>{const ok=new Set();let fin=false;const chk=()=>{if(!fin&&voters().every(x=>ok.has(x))){fin=true;res();}};
        V.check(n,rows,{canRoll:hostIn(),onConfirm:()=>{ok.add(hostName);chk();},canForce:true,onForce:()=>{fin=true;res();}});
        cur={roll:o=>{ok.add(o);chk();},leave:chk};chk();});
      cur={};const rolls=rows.map(r=>{const d=rng(),tot=d+r.val;return{owner:r.owner,d,val:r.val,tot,ok:d===20||(d!==1&&tot>=n.dc)};});
      const okc=rolls.filter(r=>r.ok).length,ok=okc*2>=rolls.length;
      const m2={t:"checkres",n:{why:n.why,dc:n.dc},rolls,ok};last.int=m2;bc(m2);await V.checkResult(n,rolls,ok,{wait:true});last.int=null;return ok;},
    async shop(n,party,listOf,buy){
      const own=owners();const msg={t:"shop",title:n.title||"ร้านค้า",list:listOf(0),voters:voters()};last.int=msg;bc(msg);
      await gather(res=>{const done=new Set();let fin=false;const chk=()=>{if(!fin&&voters().every(x=>done.has(x))){fin=true;res();}};
        const idxOf=o=>own.indexOf(o);const shopFor=o=>listOf(idxOf(o));
        let h=null;
        if(hostIn())h=V.shop(msg.title,msg.list,{gas:()=>party[idxOf(hostName)].gas||0,canShop:true,canForce:true,
          onBuy:id=>{const e=buy(idxOf(hostName),msg.list.find(x=>x.id===id));h&&h.update();return e;},onDone:()=>{done.add(hostName);h.close();chk();},onForce:()=>{fin=true;res();}});
        else h=V.shop(msg.title,msg.list,{gas:()=>0,canShop:false,canForce:true,onBuy:()=>"ไม่มีตัวละคร",onDone:()=>{},onForce:()=>{fin=true;res();}});
        cur={buy:(o,m)=>{const it=msg.list.find(x=>x.id===m.id);const e=it&&idxOf(o)>=0?buy(idxOf(o),it):"ซื้อไม่ได้";T.send(o,{t:"bought",ok:!e,err:e,id:m.id});},
             shopdone:o=>{done.add(o);chk();},leave:chk};chk();});
      cur={};last.int=null;},
    battleStart(n,Es,cnt,ally,Ps){V.battleStart(n,Es,cnt,ally,Ps);bc({t:"bstart",intro:n.intro,cnt,ally,Es,Ps,owners:owners()});},
    battleLog(L){V.battleLog(L);bc({t:"blog",L});},
    battleRefresh(Ps,Es){V.battleRefresh(Ps,Es);bc({t:"bref",Ps,Es});},
    battleEnd(){V.battleEnd();bc({t:"bend"});},
    async battleActions({Ps,Es,round,invs,flee}){
      const own=owners();const alive=Ps.map((p,i)=>p.hp>0?own[i]:null);
      const msg={t:"bmenu",round,Ps,Es,invs,flee,owners:own};last.int=msg;bc(msg);
      const acts=Ps.map(()=>null);
      await gather(res=>{let fin=false;const need=()=>Ps.map((p,i)=>i).filter(i=>Ps[i].hp>0&&connected().has(own[i]));
        const chk=()=>{if(!fin&&need().every(i=>acts[i]!==null)){fin=true;res();}};
        const hi=own.indexOf(hostName);
        if(hi>=0&&Ps[hi].hp>0)V.battleMenu({Ps,Es,round,inv:invs[hi],idx:hi,flee,canForce:true},{onAct:a=>{acts[hi]=a;chk();},onForce:()=>{need().forEach(i=>{if(acts[i]===null)acts[i]="guard";});fin=true;res();}});
        else V.battleWait&&V.battleWait("รอผู้เล่นเลือกท่า...",()=>{need().forEach(i=>{if(acts[i]===null)acts[i]="guard";});fin=true;res();});
        cur={act:(o,m)=>{const i=own.indexOf(o);if(i>=0&&Ps[i].hp>0&&acts[i]===null){acts[i]=m.a;chk();}},leave:chk};chk();});
      cur={};last.int=null;return acts;},
    async end(n,st,A,party){const sum={log:st.log,party:party.map(c=>({name:c.name,level:c.level,gas:c.gas}))};const m={t:"end",n:{text:n.text},sum};last.int=m;bc(m);await V.end(n,sum,{isHost:true});}
  };
  return ui;
}

// ---------- Client ----------
function makeClient(V,T,{name}){
  let myGas=0,h=null,chH=null,shopH=null,mine=-1;
  const me=list=>list.find(p=>p.owner===name);
  T.onMsg(m=>{switch(m.t){
    case "bg":V.bg(m.id);break;
    case "status":{const p=me(m.list);if(p)myGas=p.gas;V.status(m.list);if(shopH)shopH.update();break;}
    case "toast":V.toast(m.arr);break;
    case "say":V.say(m.n,{wait:false});break;
    case "choice":{const can=m.voters.includes(name);h=V.choice(m,{canVote:can,canClose:false,onPick:i=>{T.send({t:"vote",i});h.lock("ส่งโหวตแล้ว");}});break;}
    case "tally":h&&h.tally(m.voted,m.total);break;
    case "result":h&&h.result(m.text,m.pick);break;
    case "check":{const can=m.voters.includes(name);chH=V.check(m.n,m.vals,{canRoll:can,canForce:false,onConfirm:()=>{T.send({t:"roll"});chH.waiting&&chH.waiting("ยืนยันแล้ว รอคนอื่น...");}});break;}
    case "checkres":V.checkResult(m.n,m.rolls,m.ok,{wait:false});break;
    case "shop":{const can=m.voters.includes(name);shopH=V.shop(m.title,m.list,{gas:()=>myGas,canShop:can,canForce:false,onBuy:id=>{T.send({t:"buy",id});return null;},onDone:()=>{T.send({t:"shopdone"});shopH.close();shopH=null;}});break;}
    case "bought":V.toast([m.ok?"ซื้อแล้ว":m.err]);break;
    case "bstart":V.battleStart({intro:m.intro},m.Es,m.cnt,m.ally,m.Ps);break;
    case "blog":V.battleLog(m.L);break;
    case "bref":V.battleRefresh(m.Ps,m.Es);break;
    case "bend":V.battleEnd();break;
    case "bmenu":{const i=m.owners.indexOf(name);if(i>=0&&m.Ps[i].hp>0)V.battleMenu({Ps:m.Ps,Es:m.Es,round:m.round,inv:m.invs[i],idx:i,flee:m.flee},{onAct:a=>T.send({t:"act",a})});else V.battleWait&&V.battleWait("รอผู้เล่นคนอื่นเลือกท่า...");break;}
    case "end":V.end(m.n,m.sum,{isHost:false});break;
  }});
}
g.MP={makeSPUI,makeHostUI,makeClient};
if(typeof module!=="undefined")module.exports=g.MP;
})(typeof window!=="undefined"?window:globalThis);
