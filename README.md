# ใบเรือเงิน: คลังใต้ภูผา (ชื่อชั่วคราว)

เกมแฟนตาซีผลัดตา สไตล์ DnD ภาษาไทย รันบน GitHub Pages ล้วน ไม่มีเซิร์ฟเวอร์
GM 1 คนแชร์หน้าจอใน Discord วอยซ์ ผู้เล่นใช้การ์ดตัวละครของตัวเอง (export/import JSON)

## เปิดดูในเครื่อง
```
python3 -m http.server 8000     # แล้วเปิด http://localhost:8000
node tools/validate.js          # ตรวจข้อมูลทั้งหมด
```

## ขึ้นเว็บ
1. Settings → Pages → Source: **GitHub Actions**
2. push เข้า `main` → workflow `validate-and-deploy` ตรวจข้อมูลแล้ว deploy ให้อัตโนมัติ

## โครงสร้าง
- `data/` ข้อมูลเกมทั้งหมดเป็น JSON (เผ่า 20, อาชีพ 40, คุณลักษณะ 50, ธาตุ 9, มอนสเตอร์ 17, NPC 30, สถานที่ 30, วัตถุดิบ 100, อาหาร 41)
- `images/npc/<id>_<normal|smile|angry|sad|shock|shy>.webp`, `images/bg/<location_id>.webp`
- `js/vault.js` ระบบเซฟ 2 ชั้น (ดู docs/SAVE_SPEC.md) ทดสอบ: `node tools/test_vault.js`
- `tools/validate.js` ตรวจจำนวน/id ซ้ำ/อ้างอิง/สมดุล; `tools/build_materials.py` สร้าง materials.json
- `raw/` ข้อมูลดิบจากผู้เล่น (ไม่ถูก deploy)

## สถานะข้อมูล
- วัตถุดิบ 41 ชิ้น (`draft:true`) ยังไม่ได้รับข้อมูลจริง: ore #15, #30-50 และ herb #2-20 ฉันร่างให้ไว้ก่อน ส่งของจริงมาแล้วทับได้
- ชื่อที่ใกล้ลิขสิทธิ์ถูกเปลี่ยนแล้ว (ฟิลด์ `renamed`) และแหล่งเดิมของโรงเรียนเก็บใน `dlc_src` ไว้ DLC
- ภาพ NPC ยังเป็นชีตรวม ต้องตัดเป็น 6 อารมณ์/ตัว (ยังไม่ได้ทำ)
- repo เป็น public: ห้ามใส่ความลับของ GM ใน repo (ใช้ `gm_secrets.json` ซึ่งถูก gitignore)
