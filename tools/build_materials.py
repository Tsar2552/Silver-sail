#!/usr/bin/env python3
"""สร้าง data/materials.json + data/zones.json จาก raw/ + รายการ draft (ที่ผู้เล่นยังไม่ได้ส่ง)
รัน: python3 -I tools/build_materials.py <mat_raw.json>"""
import json,sys,re
raw=json.load(open(sys.argv[1],encoding='utf8'))
RENAME={ # ชื่อที่ใกล้ IP เกินไป -> ชื่อเกมเรา
 'Flobberworm Mucus':('Mire Worm Mucus','เมือกหนอนบึง'),
 'Acromantula Venom':('Giant Spider Venom','พิษแมงมุมยักษ์'),
 'Graphorn Horn Shard':('Horned Beast Shard','เศษเขาอสูรเขาคู่'),
 'Dementor Essence':('Wraith Essence','แก่นวิญญาณเร่ร่อน'),
 'Hippogriff Feather':('Gryphon-Steed Feather','ขนม้าปีกกริฟฟอน'),
 'Mooncalf Milk':('Moon Fawn Milk','นมลูกกวางจันทร์'),
}
ZONE_WORDS=[('ป่ามืดทึบ','deep_forest'),('ป่าต้องห้าม','deep_forest'),('เขตอนุรักษ์','beast_reserve'),('โซนต้นสน','pine_forest')]
DIR=[('เหนือ','n'),('ตะวันออก','e'),('ใต้','s'),('ตะวันตก','w')]
ORE_SRC=[('เหมืองชั้นต้น','mine_shallow'),('เหมืองชั้นกลาง','mine_mid'),('เหมืองลึก','mine_deep'),('เหมืองชั้นเวทมนต์','mine_mana'),
 ('กลางคืน','mine_night'),('ภูเขาไฟ','volcano'),('แม่น้ำ','river'),('หลอมในห้อง','workshop'),('นำsteel','workshop'),('ถ้ำโบราณ','ancient_cave'),
 ('โล้งกว้าง','windy_plain'),('หลุมอุกกาบาต','meteor_crater'),('อุกาบาต','meteor_crater'),('ป่าต้องห้ามทางเหนือ','deep_forest_n'),
 ('สุริยุปราคา','deep_forest_eclipse'),('จันทรุปราคา','deep_forest_eclipse'),('ป่าต้องห้าม','deep_forest_core'),('ดันเจี้ยนที่มี','dungeon_old'),('ดันเจี้ยน','dungeon')]
def zones(kind,src):
    z=[]
    if kind=='herb':
        for w,zz in ZONE_WORDS:
            if w in src:
                d=next((c for t,c in DIR if t in src),'')
                z.append(zz+('_'+d if d else '')); break
    else:
        for w,zz in ORE_SRC:
            if w in src: z.append(zz); break
    if 'ร้านดันเจี้ยน' in src: z.append('shop')
    return z or ['dungeon']
# draft ที่ยังขาด (ผู้เล่นยังไม่ส่ง) -> ตั้งธง draft:true ให้ GM แก้/ทับได้
D=[ # kind,n,en,th,rarity,value,desc,zone
('ore',15,'Frost Silver','เงินน้ำแข็ง','Rare',6200,'โลหะเย็นจัดที่ไม่ละลาย ใช้ทำอาวุธธาตุน้ำแข็ง','mine_deep'),
('ore',30,'Wind Quartz','ควอตซ์สายลม','Epic',23000,'ผลึกที่หมุนเบาๆ ตามลม ใช้ทำอาวุธธาตุลม','windy_plain'),
('ore',31,'Tidal Pearl Ore','แร่ไข่มุกน้ำขึ้น','Epic',24000,'แร่เรืองแสงจากก้นทะเลสาบ ใช้เสริมเกราะธาตุน้ำ','underground_lake'),
('ore',32,'Ember Core','แกนถ่านไฟ','Epic',25000,'ก้อนแร่ร้อนไม่มอด ใช้ทำอาวุธธาตุไฟ','volcano'),
('ore',33,'Gale Iron','เหล็กพายุ','Epic',26000,'เหล็กที่ผ่านพายุฟ้าผ่านับร้อยครั้ง','windy_plain'),
('ore',34,'Deep Amber','อำพันห้วงลึก','Epic',22000,'ยางไม้โบราณในถ้ำ กักเก็บเสียงกระซิบไว้','ancient_cave'),
('ore',35,'Light Prism','ปริซึมแสง','Epic',27000,'ผลึกหักเหแสงเป็นเจ็ดสี ใช้ทำอาวุธธาตุแสง','mine_mana'),
('ore',36,'Void Glass','แก้วสุญญากาศ','Epic',28000,'แก้วดำดูดแสง ใช้ทำอาวุธธาตุมืด','dungeon_old'),
('ore',37,'Titan Bone Ore','แร่กระดูกไททัน','Epic',26000,'แร่หนาแน่นสุดๆ ใช้ทำโล่หนัก','mine_deep'),
('ore',38,'Aurora Stone','หินแสงเหนือ','Legendary',32000,'หินที่เปล่งแสงหลากสีตอนกลางคืน','mine_night'),
('ore',39,'Dragon Scale Ore','แร่เกล็ดมังกร','Legendary',35000,'แร่ที่ขึ้นเป็นเกล็ดตามรอยแยก','volcano'),
('ore',40,'Star Iron','เหล็กดวงดาว','Legendary',36000,'เหล็กจากดาวตกที่แข็งแกร่งกว่าเหล็กอุกกาบาต','meteor_crater'),
('ore',41,'Abyss Silver','เงินห้วงอเวจี','Legendary',38000,'เงินที่ดูดซับความมืดจนดำสนิท','dungeon_old'),
('ore',42,'Saint Gold','ทองศักดิ์สิทธิ์','Legendary',40000,'ทองที่ผ่านพิธีอธิษฐานหนึ่งร้อยปี','ancient_cave'),
('ore',43,'Thunder Heart','หัวใจอัสนี','Legendary',42000,'แกนฟ้าผ่าที่ยังเต้นอยู่','mine_deep'),
('ore',44,'Frozen Sun','ตะวันเยือกแข็ง','Legendary',45000,'แร่ขัดแย้งในตัวเอง ร้อนและเย็นพร้อมกัน','deep_forest_eclipse'),
('ore',45,'Orichalcum','ออริชัลคัม','Relic',90000,'โลหะในตำนาน ว่ากันว่ามาจากทวีปที่จมหาย','ancient_cave'),
('ore',46,'Skyfall Alloy','โลหะฟ้าถล่ม','Relic',110000,'โลหะผสมจากอุกกาบาตสามก้อนที่ตกคืนเดียวกัน','meteor_crater'),
('ore',47,'Worldroot Crystal','ผลึกรากโลก','Relic',130000,'ผลึกที่เชื่อมรากไม้ทุกต้นเข้าด้วยกัน','deep_forest_core'),
('ore',48,'Eternal Flame Stone','หินเพลิงนิรันดร์','Relic',150000,'ไฟที่ไม่เคยดับตั้งแต่ก่อนมีอารยธรรม','volcano'),
('ore',49,'Moonlit Mithril','มิธริลต้องแสงจันทร์','Relic',170000,'มิธริลที่ผ่านคืนจันทร์เต็มดวงนับพัน','deep_forest_eclipse'),
('ore',50,'Heart of the Mountain','หัวใจแห่งภูผา','Relic',250000,'แร่ที่ว่ากันว่าเป็นหัวใจของคลังใต้ภูผา','dungeon_deep'),
('herb',2,'Valerian Root','รากวาเลเรียน','Common',500,'รากไม้กลิ่นฉุน ใช้ในยากล่อมประสาท','pine_forest_n'),
('herb',3,'Moss Cap','หมวกตะไคร่','Common',500,'เห็ดตะไคร่ ใช้ในยาห้ามเลือดเบื้องต้น','outskirt_forest'),
('herb',4,'Bog Reed','กกบึง','Common',500,'ต้นกกที่ดูดน้ำยาได้ดี','deep_forest_s'),
('herb',5,'Sunpetal','ดอกตะวัน','Common',600,'กลีบดอกที่ให้ความอบอุ่นอ่อนๆ','outskirt_forest'),
('herb',6,'Ghost Thistle','ผักเสี้ยนผี','Uncommon',1000,'พืชหนามเรืองแสงจางๆ ใช้ในยาล่องหน','deep_forest_w'),
('herb',7,'Ember Pepper','พริกถ่านไฟ','Uncommon',1100,'พริกที่เผาลิ้นสามวัน ใช้ในยาเสริมแรง','deep_forest_s'),
('herb',8,'Silvervine','เถาเงิน','Uncommon',1200,'เถาวัลย์ที่แมวหลงรัก','pine_forest_n'),
('herb',9,'Nightshade Berry','ผลไนท์เชด','Uncommon',1200,'ผลไม้พิษอ่อนๆ ใช้ในยาสลบ','deep_forest_w'),
('herb',10,'Frost Lily','ลิลลี่น้ำแข็ง','Uncommon',1300,'ดอกไม้ที่บานเฉพาะอากาศหนาว','pine_forest_n'),
('herb',11,'Quicksilver Moss','ตะไคร่ปรอท','Uncommon',1400,'ตะไคร่ที่ไหลได้ ใช้ในยาเร่งความเร็ว','beast_reserve_e'),
('herb',12,'Giant Spider Silk','ใยแมงมุมยักษ์','Rare',3000,'ใยเหนียวหนึบ ใช้ในยาสมานแผลลึก','deep_forest_w'),
('herb',13,'Thornroot','รากหนามเหล็ก','Rare',3200,'รากแข็งเป็นหนาม ใช้ในยาเสริมเกราะ','deep_forest_s'),
('herb',14,'Bloodmoss','ตะไคร่เลือด','Rare',3300,'ตะไคร่แดงใช้ในยาเพิ่มเลือด','deep_forest_core'),
('herb',15,'Windflower','ดอกลมพัด','Rare',3500,'ดอกไม้หมุนตามลม ใช้ในยาเพิ่มความเร็ว','beast_reserve_e'),
('herb',16,'Serpent Scale Dust','ผงเกล็ดงู','Rare',3600,'ผงละเอียดจากเกล็ดงูใหญ่ ใช้ในยาต้านพิษ','deep_forest_s'),
('herb',17,'Dusk Lotus','บัวสนธยา','Rare',3800,'บัวที่บานเฉพาะยามเย็น ใช้ในยาสงบจิต','underground_lake'),
('herb',18,'Troll Sweat','เหงื่อโทรลล์','Rare',3900,'ของเหม็นแต่ฟื้นฟูแผลเร็ว','beast_reserve_s'),
('herb',19,'Pixie Dust','ผงภูตจิ๋ว','Rare',4200,'ผงเรืองแสง ใช้ในยาลอยตัว','pine_forest_n'),
('herb',20,'Griffin Egg Shell','เปลือกไข่กริฟฟอน','Rare',4300,'เปลือกแข็งใช้ในยาเสริมกำลังขา','beast_reserve_n'),
]
out=[];seen=set()
for r in raw:
    en,th=RENAME.get(r['en'],(r['en'],r['th']))
    mid=re.sub(r'[^a-z0-9]+','_',en.lower()).strip('_')
    out.append(dict(id=mid,kind=r['kind'],no=r['n'],en=en,th=th,rarity=r['rarity'],value=r['value'],desc=r['desc'],
        zones=zones(r['kind'],r['src']),dlc_src=r['src'],draft=False,renamed=r['en'] in RENAME))
for k,n,en,th,ra,v,ds,z in D:
    out.append(dict(id=re.sub(r'[^a-z0-9]+','_',en.lower()).strip('_'),kind=k,no=n,en=en,th=th,rarity=ra,value=v,desc=ds,
        zones=[z],dlc_src='',draft=True,renamed=False))
for m in out:
    assert m['id'] not in seen,m['id']; seen.add(m['id'])
out.sort(key=lambda m:(m['kind'],m['no']))
json.dump({'_note':'วัตถุดิบ 100 ชิ้น: ore 1-50 (แร่/อัญมณี) herb 1-50 (วัตถุดิบยา). draft:true = ข้อมูลที่ยังไม่ได้รับจากผู้เล่น ฉันร่างให้ แก้ทับได้. dlc_src = แหล่งเดิมของโรงเรียน (ไว้ DLC)','materials':out},open('data/materials.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
zs=sorted({z for m in out for z in m['zones']})
json.dump({'_note':'โซนเก็บวัตถุดิบในเกมหลัก (ใช้แทนแหล่งของโรงเรียน)','zones':zs},open('data/zones.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print(len(out),sum(m['draft'] for m in out),'draft;',len(zs),'zones')
