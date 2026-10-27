// ตรวจความถูกต้องของข้อมูลเกม: node tools/validate.js
const fs = require("fs");
const path = require("path");
const rd = n => JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", n + ".json"), "utf8"));
let errors = 0, warns = 0;
const err = m => { console.error("ERROR  " + m); errors++; };
const warn = m => { console.warn("WARN   " + m); warns++; };
const uniq = (arr, label) => { const s = new Set(); arr.forEach(x => { if (s.has(x)) err(`${label}: id ซ้ำ ${x}`); s.add(x); }); };

const races = rd("races"), el = rd("elements"), cls = rd("classes"), tr = rd("traits"),
      npcs = rd("npcs"), mon = rd("monsters"), loc = rd("locations"), misc = rd("misc");

// จำนวนตามเป้า
const want = { races: 20, classes: 40, traits: 50, npcs: 30, monsters: 17, locations: 30, elements: 9 };
const got = { races: races.races.length, classes: cls.classes.length, traits: tr.traits.length,
  npcs: npcs.npcs.length, monsters: mon.monsters.length, locations: loc.locations.length, elements: el.elements.length };
for (const k in want) if (got[k] !== want[k]) err(`จำนวน ${k} = ${got[k]} ควรเป็น ${want[k]}`);

uniq(races.races.map(r => r.id), "races");
uniq(cls.classes.map(c => c[0]), "classes");
uniq(tr.traits.map(t => t[0]), "traits");
uniq(npcs.npcs.map(n => n.id), "npcs");
uniq(mon.monsters.map(m => m[0]), "monsters");
uniq(loc.locations.map(l => l[0]), "locations");

const elIds = new Set(el.elements.map(e => e.id));
el.elements.forEach(e => {
  if (e.strong && !elIds.has(e.strong)) err(`ธาตุ ${e.id}: strong ไม่มี ${e.strong}`);
  if (e.weak && !elIds.has(e.weak)) err(`ธาตุ ${e.id}: weak ไม่มี ${e.weak}`);
});

// เผ่า: สเตตัสครบ 9 ค่า ช่วงรวมสมเหตุสมผล (HP /10)
const sums = [];
races.races.forEach(r => {
  if (r.stats.length !== 9) err(`เผ่า ${r.id}: สเตตัสไม่ครบ 9`);
  if (r.stats.some(v => !Number.isFinite(v) || v < 0)) err(`เผ่า ${r.id}: สเตตัสผิด`);
  if (r.element && !elIds.has(r.element)) err(`เผ่า ${r.id}: ธาตุไม่มี ${r.element}`);
  if (!r.can_eat.length) err(`เผ่า ${r.id}: ไม่มีอาหารที่กินได้`);
  const sum = r.stats.reduce((a, b, i) => a + (i === 2 ? b / 10 : b), 0);
  sums.push([r.id, sum]);
});
const avg = sums.reduce((a, b) => a + b[1], 0) / sums.length;
sums.forEach(([id, s]) => { if (Math.abs(s - avg) > 12) warn(`บาลานซ์: เผ่า ${id} รวม ${s} ห่างจากค่าเฉลี่ย ${avg.toFixed(1)} เกิน 12`); });

// อาชีพ/คุณลักษณะ: คีย์โบนัสต้องเป็นสเตตัสจริง และมีคำอธิบาย
const stats = new Set(["p_atk", "m_atk", "hp", "spd", "p_def", "m_def", "luck", "wit", "mana"]);
cls.classes.forEach(c => {
  Object.keys(c[3]).forEach(k => { if (!stats.has(k)) err(`อาชีพ ${c[0]}: คีย์โบนัสผิด ${k}`); });
  if (!c[4]) err(`อาชีพ ${c[0]}: ไม่มีคำอธิบายสกิล`);
});
tr.traits.forEach(t => { if (!t[3]) err(`คุณลักษณะ ${t[0]}: ไม่มีคำอธิบาย`); });

// มอนสเตอร์
mon.monsters.forEach(m => {
  if (m[10] && !elIds.has(m[10])) err(`มอนสเตอร์ ${m[0]}: ธาตุไม่มี ${m[10]}`);
  if (m[11] && !elIds.has(m[11])) err(`มอนสเตอร์ ${m[0]}: จุดอ่อนไม่มี ${m[11]}`);
  if (!m[10] && m[11]) err(`มอนสเตอร์ ${m[0]}: ไม่มีธาตุแต่มีจุดอ่อน (กติกา: ไม่มีธาตุ = ไม่มีจุดอ่อน)`);
});

// สุ่มตัวละคร: ตารางกลัวต้องมีอย่างน้อย 1 ตัวเหลือต่อเผ่า
const fearIds = misc.fears.map(f => f[0]);
races.races.forEach(r => {
  const ex = misc.fear_exclude[r.id] || [];
  if (fearIds.filter(f => !ex.includes(f)).length === 0) err(`เผ่า ${r.id}: ไม่เหลือสิ่งที่กลัวให้สุ่ม`);
});

// อาหาร: ทุกเผ่าต้องมีของกิน (ตรวจแท็กพื้นฐานเมื่อมีไฟล์อาหาร)
const foodFile = path.join(__dirname, "..", "data", "food.json");
if (fs.existsSync(foodFile)) {
  const food = JSON.parse(fs.readFileSync(foodFile, "utf8")).food || [];
  races.races.forEach(r => {
    const n = food.filter(f => f.tags.some(t => r.can_eat.includes(t)) && !f.tags.some(t => r.cannot_eat.includes(t))).length;
    if (n < 3) warn(`เผ่า ${r.id}: กินได้เพียง ${n} ชนิด (ควร ≥ 3)`);
  });
}


// วัตถุดิบ: id ไม่ซ้ำ, โซนต้องมีอยู่, ครบ 50+50
const matFile = path.join(__dirname, "..", "data", "materials.json");
if (fs.existsSync(matFile)) {
  const mats = JSON.parse(fs.readFileSync(matFile, "utf8")).materials;
  const zones = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "zones.json"), "utf8")).zones;
  const ids = new Set();
  mats.forEach(m => {
    if (ids.has(m.id)) err(`วัตถุดิบ id ซ้ำ: ${m.id}`); ids.add(m.id);
    m.zones.forEach(z => { if (z !== "shop" && !zones.includes(z)) err(`วัตถุดิบ ${m.id}: โซน ${z} ไม่มีใน zones.json`); });
  });
  ["ore", "herb"].forEach(k => { const n = mats.filter(m => m.kind === k).length; if (n !== 50) err(`วัตถุดิบ ${k} ต้อง 50 ชิ้น มี ${n}`); });
  const d = mats.filter(m => m.draft).length;
  if (d) warn(`วัตถุดิบ ${d} ชิ้นยังเป็น draft (รอข้อมูลจริงจากผู้เล่น)`);
}

// ภาพ NPC (เตือนเท่านั้น เพราะภาพทยอยใส่)
const emos = ["normal", "smile", "angry", "sad", "shock", "shy"];
let missing = 0;
npcs.npcs.forEach(n => emos.forEach(e => {
  if (!fs.existsSync(path.join(__dirname, "..", "images", "npc", `${n.id}_${e}.webp`))) missing++;
}));
if (missing) warn(`ภาพ NPC ยังขาด ${missing} จาก ${npcs.npcs.length * emos.length} ภาพ (ใช้ตัวอักษรแทนไปก่อน)`);

console.log(`\nตรวจเสร็จ: ${errors} ข้อผิดพลาด, ${warns} คำเตือน`);
console.log(`เผ่า ${got.races} | อาชีพ ${got.classes} | คุณลักษณะ ${got.traits} | NPC ${got.npcs} | มอนสเตอร์ ${got.monsters} | สถานที่ ${got.locations} | ธาตุ ${got.elements}`);
process.exit(errors ? 1 : 0);
