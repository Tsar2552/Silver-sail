#!/usr/bin/env python3
"""ลบพื้นขาว/ขอบการ์ด/ป้ายอารมณ์ ออกจากภาพ NPC -> webp โปร่งใส
python3 -I tools/make_transparent.py <indir> <outdir>"""
import sys,os,glob,numpy as np,cv2
src,dst=sys.argv[1],sys.argv[2];os.makedirs(dst,exist_ok=True)
def process(path):
    im=cv2.imread(path,cv2.IMREAD_COLOR);h,w=im.shape[:2]
    # 1) ลบป้ายอารมณ์ (กล่องดำมุมซ้ายบน) ด้วย inpaint
    dark=(im.max(axis=2)<60).astype(np.uint8)
    win=np.zeros_like(dark);win[:int(h*.13),:int(w*.42)]=1
    dm=cv2.morphologyEx(dark*win,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    tag=np.zeros((h,w),np.uint8)
    for sx,sy in [(int(w*fx),int(h*fy)) for fy in (.03,.04,.05,.06,.07,.08,.09,.10) for fx in (.035,.045,.06)]:
        if dm[sy,sx]:
            f=np.zeros((h+2,w+2),np.uint8);wk=dm.copy();cv2.floodFill(wk,f,(sx,sy),2)
            ys,xs=np.where(wk==2)
            if len(xs)>300:
                tag[max(0,ys.min()-3):ys.max()+4,max(0,xs.min()-3):xs.max()+4]=1;break
    if tag.any():im[tag>0]=255   # เติมขาว แล้วให้ขั้นลบพื้นหลังทำให้โปร่งใสต่อ
    # 2) ตัดขอบการ์ด
    m=int(min(h,w)*.012);im=im[m:h-m,m:w-m];h,w=im.shape[:2]
    # 3) พื้นหลัง = พิกเซลเกือบขาวที่เชื่อมกับขอบภาพ
    white=(im.min(axis=2)>=244).astype(np.uint8)
    # ปิดช่องเส้นขอบบางๆ ที่ติดขอบ: ขอบการ์ดสีเทา/ดำบางเส้นบังไม่ให้ flood ไปถึง
    pad=cv2.copyMakeBorder(white,1,1,1,1,cv2.BORDER_CONSTANT,value=1)
    flood=np.zeros((h+4,w+4),np.uint8);work=pad.copy()
    cv2.floodFill(work,flood,(0,0),2)
    bg=(work[1:-1,1:-1]==2)
    # เพิ่มจุดเริ่มอื่นตามขอบ เผื่อมุมถูกบัง
    for x in range(0,w,max(1,w//40)):
        for y in (0,h-1):
            if white[y,x] and not bg[y,x]:
                f2=np.zeros((h+2,w+2),np.uint8);wk=white.copy();cv2.floodFill(wk,f2,(x,y),2);bg|=(wk==2)
    for y in range(0,h,max(1,h//40)):
        for x in (0,w-1):
            if white[y,x] and not bg[y,x]:
                f2=np.zeros((h+2,w+2),np.uint8);wk=white.copy();cv2.floodFill(wk,f2,(x,y),2);bg|=(wk==2)
    fg=(~bg).astype(np.uint8)
    # ตัดเศษเล็กๆ (เก็บเฉพาะก้อนใหญ่ + ไอคอนอารมณ์ที่มีสี)
    n,lab,stats,_=cv2.connectedComponentsWithStats(fg,connectivity=8)
    keep=np.zeros_like(fg)
    big=max(stats[1:,4]) if n>1 else 0
    for i in range(1,n):
        x,y,ww,hh,ar=stats[i]
        if ar<big*0.03 and y<h*.10 and x<w*.45:continue   # เศษป้าย/ขอบการ์ดมุมซ้ายบน
        if ar>=max(150,big*0.0008):keep[lab==i]=1
    fg=keep
    # ปิดรูพื้นหลังที่ถูกล้อมโดยตัวละคร (เช่นช่องระหว่างแขน) ไม่ลบ เก็บเป็นขาวเดิมเพื่อไม่ให้เป็นรู
    fg=cv2.morphologyEx(fg,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    fg=cv2.erode(fg,np.ones((3,3),np.uint8),iterations=1)
    a=cv2.GaussianBlur(fg.astype(np.float32),(0,0),0.9)
    a=np.clip(a*1.15-0.08,0,1)
    out=np.dstack([im,(a*255).astype(np.uint8)])
    # ตัดพื้นที่โปร่งใสรอบนอก
    ys,xs=np.where(a>0.05)
    if len(xs):out=out[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return out
for f in sorted(glob.glob(os.path.join(src,'*.webp'))):
    o=process(f);cv2.imwrite(os.path.join(dst,os.path.basename(f)),o,[cv2.IMWRITE_WEBP_QUALITY,90])
print('done',len(glob.glob(os.path.join(dst,'*.webp'))))
