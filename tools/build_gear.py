#!/usr/bin/env python3
"""สร้าง data/weapons.json, armor.json, statuses.json  (รัน: python3 -I tools/build_gear.py)"""
import json
EL={'earth':'ดิน','water':'น้ำ','wind':'ลม','fire':'ไฟ','metal':'โลหะ','lightning':'สายฟ้า','light':'แสง','dark':'มืด','ice':'น้ำแข็ง'}
ORE={'earth':'granite','water':'tidal_pearl_ore','wind':'wind_quartz','fire':'ember_core','metal':'black_steel','lightning':'thunder_ore','light':'light_prism','dark':'shadow_stone','ice':'frost_silver'}
# id, ไทย, พลัง T1, ใช้สเตตัสเล็ง, มือ, คำอธิบาย
WT=[('sword','ดาบ',3,'p',1,'สมดุล ใช้ง่าย'),('greatsword','ดาบใหญ่',4,'p',2,'หนัก แรง ช้า'),('dagger','มีดสั้น',2,'p',1,'เบา ไว ติดคริติคอลง่าย'),
('spear','หอก',3,'p',2,'โจมตีเหนือกว่าผู้ใกล้'),('axe','ขวาน',4,'p',1,'ฟันเกราะแตก'),('hammer','ค้อน',4,'p',2,'ทุบหนัก ทำมึนงงได้'),
('bow','ธนู',3,'p',2,'โจมตีระยะไกล'),('crossbow','หน้าไม้',4,'p',2,'ยิงแรง เติมกระสุนช้า'),('claw','กรงเล็บ',3,'p',1,'เหมาะสายต่อสู้มือเปล่า'),
('staff','คทา',3,'m',2,'ขยายพลังเวท ฟื้น MANA'),('wand','ไม้กายสิทธิ์',2,'m',1,'เวทไว ร่ายต่อเนื่อง')]
TIER=[('common','Common',1,0,1.0,400),('uncommon','Uncommon',5,1,1.8,1500),('rare','Rare',10,2,3.2,7000)]
W=[]
def prefix(t): return {'common':'เหล็ก','uncommon':'เหล็กกล้า','rare':'เหล็กวิเศษ'}[t]
for tid,th,p,stat,hands,desc in WT:
    for t,rar,lv,_,mul,price in TIER:
        if t=='rare':
            for e,eth in EL.items():
                W.append(dict(id=f'{tid}_{t}_{e}',th=f'{th}ธาตุ{eth}',type=tid,type_th=th,rarity=rar,level=lv,power=round(p*mul),stat=stat,hands=hands,element=e,price=price+(1500 if hands==2 else 0),material=ORE[e],desc=f'{desc} / ผนึกพลังธาตุ{eth}'))
        else:
            W.append(dict(id=f'{tid}_{t}',th=f'{th}{prefix(t)}',type=tid,type_th=th,rarity=rar,level=lv,power=round(p*mul),stat=stat,hands=hands,element=None,price=price+(150 if hands==2 else 0)*(1 if t=='common' else 3),material='steel' if t=='uncommon' else None,desc=desc))
AT=[('light','เกราะเบา',2,1,0,1,'ขยับตัวคล่อง ไม่ลด SPD'),('medium','เกราะกลาง',4,2,5,0,'สมดุล'),('heavy','เกราะหนัก',7,2,15,-1,'ทนทานแต่ลด SPD'),
('robe','เสื้อคลุมเวท',1,5,0,0,'ต้านเวท เสริม MANA'),('shield','โล่',3,2,0,0,'ถือมือเดียว +P DEF (ไม่ใช้คู่อาวุธ 2 มือ)')]
A=[]
for tid,th,pd,md,hp,spd,desc in AT:
    for t,rar,lv,_,mul,price in TIER:
        if t=='rare':
            for e,eth in EL.items():
                A.append(dict(id=f'{tid}_{t}_{e}',th=f'{th}ธาตุ{eth}',type=tid,type_th=th,rarity=rar,level=lv,p_def=round(pd*mul),m_def=round(md*mul),hp=round(hp*mul)*10,spd=spd*2 if spd<0 else 0,resist=e,price=price+500,material=ORE[e],desc=f'{desc} / ต้านธาตุ{eth} (ลดดาเมจ 25%)'))
        else:
            A.append(dict(id=f'{tid}_{t}',th=f'{th}{prefix(t)}',type=tid,type_th=th,rarity=rar,level=lv,p_def=round(pd*mul),m_def=round(md*mul),hp=round(hp*mul)*10,spd=spd if t=='common' else spd*2 if spd<0 else 0,resist=None,price=price,material='steel' if t=='uncommon' else None,desc=desc))
S=[('poison','พิษ','เสีย HP 5% ทุกเทิร์น 3 เทิร์น','ยาถอนพิษ / ศาลเจ้า'),('burn','ไหม้','เสีย HP 8% ทุกเทิร์น และ P ATK −10%','น้ำ / ยาแก้ไหม้'),
('freeze','แช่แข็ง','ข้ามเทิร์น 1 ครั้ง ดาเมจไฟต่อเป้านี้ x1.5 แล้วหาย','ความร้อน / ตีแรง'),('paralyze','ชา','SPD −50% 2 เทิร์น (แมงมุมยักษ์ใช้บ่อย)','ยาแก้ชา'),
('sleep','หลับ','ข้ามเทิร์น ตื่นเมื่อโดนตี','โดนตี / น้ำเย็น'),('stun','มึนงง','เสีย 1 เทิร์น ไม่ซ้อนกัน','รอ 1 เทิร์น'),('bleed','เลือดไหล','เสีย HP 6% ทุกเทิร์น จนกว่าจะพันแผล','ผ้าพันแผล / ฮีล'),
('curse','คำสาป','LUCK −3 และฟื้น HP ครึ่งเดียว','พระ / ยาถอนคำสาป'),('fear','หวาดกลัว','ทอยโจมตีมีเสียเปรียบ ถ้าเจอสิ่งที่กลัว','เพื่อนปลอบ / ผ่านการทอย WIT'),
('blind','ตาบอด','ทอยเล็งมีเสียเปรียบ','น้ำล้างตา'),('slow','ช้า','SPD −30% 3 เทิร์น','รอ'),('silence','ปิดเสียง','ร่ายเวทไม่ได้ 2 เทิร์น','ยาเปิดคอ'),
('weaken','อ่อนแรง','P ATK และ M ATK −20% 3 เทิร์น','พัก / ยา'),('regen','ฟื้นฟู','ฟื้น HP 5% ทุกเทิร์น 3 เทิร์น','—'),('shield','โล่เวท','ลดดาเมจรับ 30% 2 เทิร์น','—'),
('rage','คลุ้มคลั่ง','P ATK +30% แต่ P DEF −20% 3 เทิร์น','พัก'),('down','ล้มลง (HP 0)','ทอย Death Save: 10+ รอด ต่ำกว่านั้นสะสมความล้มเหลว 3 ครั้งตาย','ฮีลหรือยาฟื้นชีพ')]
json.dump({'_note':'อาวุธ 11 ชนิด x (Common, Uncommon, Rare x 9 ธาตุ) สร้างด้วย tools/build_gear.py','weapons':W},open('data/weapons.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
json.dump({'_note':'เกราะ 5 ชนิด x (Common, Uncommon, Rare x 9 ธาตุ)','armor':A},open('data/armor.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
json.dump({'statuses':[dict(id=a,th=b,effect=c,cure=d) for a,b,c,d in S]},open('data/statuses.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print(len(W),len(A),len(S))
