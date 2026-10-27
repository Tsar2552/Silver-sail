#!/usr/bin/env python3
"""ตัดชีตอารมณ์ NPC (3x2: ปกติ ยิ้ม โกรธ / เศร้า ตกใจ เขิน) -> images/npc/<id>_<emo>.webp
รัน: python3 -I tools/slice_npc.py <mapping.json> <outdir>   mapping = [[sheet_path, npc_id], ...]"""
import json,sys,os
from PIL import Image
EMO=['normal','smile','angry','sad','shock','shy']
COLS=[(.016,.320),(.337,.663),(.682,.990)]
ROWS=[(.008,.451),(.465,.870)]
m=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
for path,nid in m:
    im=Image.open(path).convert('RGB');w,h=im.size;k=0
    for r in ROWS:
        for c in COLS:
            p=im.crop((int(c[0]*w),int(r[0]*h),int(c[1]*w),int(r[1]*h)))
            p=p.resize((int(p.width*720/p.height),720),Image.LANCZOS)
            p.save(os.path.join(out,f'{nid}_{EMO[k]}.webp'),quality=88);k+=1
print(len(m),'sheets ->',len(m)*6,'images')
