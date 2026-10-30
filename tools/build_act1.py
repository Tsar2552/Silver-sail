#!/usr/bin/env python3
"""สร้าง data/story/act1.json  (python3 -I tools/build_act1.py)
node: say/narr(ข้อความ) choice(3 ตัวเลือก) check(ทอย d20) battle shop jump end ; do={gas,exp,item,flag,unflag,root,heal,ally,rest}"""
import json
L=[]
def add(n): L.append(n); return n
def say(sp,text,emo='normal',id=None,bg=None,do=None): return add(dict(t='say',sp=sp,emo=emo,text=text,id=id,bg=bg,do=do))
def nar(text,id=None,bg=None,do=None): return add(dict(t='narr',text=text,id=id,bg=bg,do=do))
def opt(text,goto,long=False,do=None,note=None): return dict(text=text,goto=goto,long=long,do=do,note=note)
def choice(prompt,opts,id=None,bg=None,sp=None):
    assert len(opts)==3,prompt; return add(dict(t='choice',prompt=prompt,opts=opts,id=id,bg=bg,sp=sp))
def check(stat,dc,why,ok,fail,id=None,bg=None,adv=None): return add(dict(t='check',stat=stat,dc=dc,why=why,ok=ok,fail=fail,id=id,bg=bg,adv=adv))
def battle(enemies,win,lose,id=None,bg=None,ally=None,prep=None,intro=None,flee=None): return add(dict(t='battle',enemies=enemies,win=win,lose=lose,id=id,bg=bg,ally=ally,prep=prep,intro=intro,flee=flee))
def shop(items,next,id=None,bg=None,title=None): return add(dict(t='shop',items=items,next=next,id=id,bg=bg,title=title))
def jump(cases,default,id=None): return add(dict(t='jump',cases=cases,next=default,id=id))
def end(text,id='END'): return add(dict(t='end',text=text,id=id))
def go(id,nxt): return add(dict(t='jump',cases=[],next=nxt,id=id))

# ============ บทที่ 1: หน้ากิลด์ ============
nar("ฝนพรำบนท่าเรือเมืองใบเรือเงิน ป้ายกิลด์สีเงินแกว่งไกวตามลมทะเล วันนี้คือวันแรกที่คุณมาลงทะเบียนเป็นนักผจญภัย",id='start',bg='guild_lobby',do={'gasmin':150,'item':{'bread':0}})
nar("หน้าประตูกิลด์ มีชายตาบอดนั่งถือชามเก่าๆ ศีรษะเอียงตามเสียงฝีเท้าของคุณ")
say('grong',"เสียงรองเท้าเธอ... มือใหม่สินะ ก้าวสั้น ลังเล แต่หัวใจหนักแน่น",'normal')
choice("คุณจะทำอย่างไรกับลุงโกร่ง?",[
 opt("ใส่เหรียญ 10 กัสลงในชาม","g_help",do={'gas':-10,'flag':['helped_grong']}),
 opt("ถามว่าเขารู้ได้ยังไงว่าเป็นมือใหม่","g_ask"),
 opt("เดินผ่านเข้าไปเงียบๆ","g_ignore",do={'flag':['ignored_grong']})],id='c_grong')
say('grong',"ขอบใจ... ใจดีแบบนี้ ระวังจะอายุสั้นนะ ฮ่าๆ ฟังไว้ ถ้าเจอห้องที่พื้นเสียงกลวง อย่าเหยียบตรงกลาง",'smile',id='g_help')
go('g_help2','mint')
say('grong',"คนที่ยืนหน้าประตูนี้ทุกวันฟังรองเท้าคนมานับพัน พวกกลับมา ก้าวหนักขึ้น พวกไม่กลับ ก้าวเบาลงเรื่อยๆ ... วันนี้เธอก้าวสั้นเพราะกลัว นั่นดี คนไม่กลัวตายเร็ว",'normal',id='g_ask',do={'flag':['grong_hint']})
go('g_ask2','mint')
nar("ลุงโกร่งยิ้มบางๆ ราวกับได้ยินเสียงคุณเดินผ่านไปแล้ว",id='g_ignore')
say('mint',"พี่คะ! พี่เป็นคนที่จะลงเหมืองใช่ไหมคะ... หนูได้ยินพี่ลินเด้คุยกัน",'shock',id='mint',bg='guild_lobby')
say('mint',"คนที่ไปเหมืองไม่ค่อยกลับ... พ่อหนูก็ไปแล้ว",'sad')
choice("มิ้นท์จ้องคุณตาแป๋ว เด็กน้อยกำชายเสื้อไว้แน่น",[
 opt("\"พี่สัญญา จะกลับมาให้ได้\" (รับปากเต็มที่)","m_prom",long=True,do={'root':{'mint':'promised'}},note="ถ้าผิดสัญญา มิ้นท์จะจำไปตลอด"),
 opt("\"พี่ไม่รับปาก แต่จะพยายามที่สุด\"","m_try",long=True,do={'root':{'mint':'tried'}}),
 opt("ลูบหัวเธอแล้วไม่ตอบ","m_none",do={'root':{'mint':'silent'}})],id='c_mint')
say('mint',"จริงนะคะ! งั้นหนูจะรอ... พี่เอาขนมปังจากร้านป้าแมกกี้กลับมาให้หนูด้วยนะ!",'smile',id='m_prom')
go('m_prom2','counter')
say('mint',"อื้อ... ซื่อสัตย์ดี หนูชอบ",'normal',id='m_try')
go('m_try2','counter')
nar("มิ้นท์ก้มหน้าไม่พูดอะไรอีก",id='m_none')

# ============ บทที่ 2: เคาน์เตอร์ ============
say('maren',"เซ็นตรงนี้ค่ะ ไม่ใช่ตรงนั้น ค่าใบอนุญาตหนึ่งร้อยกัสนะคะ ไม่ลดค่ะ",'normal',id='counter',bg='guild_counter')
say('linde',"ยินดีต้อนรับสู่ใบเรือเงิน ฉันลินเด้ ดูแลบัญชี ... อ้อ กิลด์มี 'สัญญากู้ยืมนักผจญภัยใหม่' ด้วย กำไรสุทธิ ไม่ใช่ยอดขาย ดอกเบี้ยเราคิดแฟร์ ใช่ไหมคะมาเรน",'smile')
say('maren',"...ค่ะ ฉันไม่อยากยุ่ง",'normal')
choice("คุณมีเงิน 150 กัส ค่าใบอนุญาตหมดไป 100 กัส ลินเด้ยื่นสัญญามาให้ดู",[
 opt("ไม่กู้ ใช้เงินที่มีอยู่","l_none",long=True,do={'gas':-100,'root':{'debt':'none'}},note="เหลือ 50 กัส ซื้อของไม่ค่อยได้ แต่ไม่มีหนี้"),
 opt("กู้ 500 กัส (คืน 600 ตอนจบ Act)","l_small",long=True,do={'gas':400,'root':{'debt':'small'}}),
 opt("กู้ 2,000 กัส (คืน 2,600 ตอนจบ Act)","l_big",long=True,do={'gas':1900,'root':{'debt':'big'}},note="ซื้อของดีได้ แต่ต้องใช้คืนก่อนจบ Act")],id='c_loan')
say('linde',"ตัดสินใจรอบคอบดี... แต่ถ้าเป็นหนี้ ฉันไม่เคยลืม",'normal',id='l_none')
go('l_none2','briefing')
say('linde',"ลงชื่อตรงนี้ค่ะ ฉันจะจดไว้ในบัญชี ขอให้โชคดีนะคะ",'smile',id='l_small')
go('l_small2','briefing')
say('linde',"โอ้... ชอบความกล้าแบบนี้ สัญญาฉบับใหญ่ ฉันเตรียมไว้แล้ว",'smile',id='l_big')
say('maren',"...ของเยอะขึ้นก็จริง แต่ใบเรือเงินไม่ใช่การกุศลนะคะ",'normal')

# ============ บทที่ 3: ภารกิจ ============
say('horka',"ของกิลด์ ต้องกลับมาครบ... รวมถึงคนด้วย",'normal',id='briefing',bg='guild_master_room')
say('horka',"เหมืองใต้ภูผาที่ปิดมาสิบปี กลับมามีเสียงดังจากข้างใน คนงานหายไปเจ็ดคน วันก่อน วาเลนซ์ รุ่นพี่เรากลับออกมาคนเดียว เขาไม่ยอมพูดอะไร",'normal')
say('horka',"ภารกิจของเจ้าคือลงไปคลังใต้ภูผา ตามหาคนงาน และหาให้ได้ว่าเกิดอะไรขึ้น ใครจะไปด้วยก็ได้",'normal')
choice("ฮอร์ก้าชี้ไปที่คาเรลและไรเวนที่ยืนอยู่ข้างๆ \"เลือกเอา\"",[
 opt("\"ข้าจะเป็นหัวหน้าทีมเอง\" (พาคาเรลและไรเวนไป)","t_lead",long=True,do={'flag':['ally_karel','ally_raven'],'ally':'karel','root':{'lead':'self'}},note="ไรเวนจะมองคุณเป็นคู่แข่งตัวจริง"),
 opt("\"ขอให้คาเรลนำทางได้ไหม\"","t_karel",long=True,do={'flag':['ally_karel'],'ally':'karel','root':{'lead':'karel'}},note="คาเรลไว้ใจคุณมากขึ้น ไรเวนจะไปทางของเขาเอง"),
 opt("\"ข้าไปคนเดียว\" (ได้ยาเพิ่ม 2 ขวด แต่ไม่มีใครช่วย)","t_solo",long=True,do={'flag':['lone_wolf'],'item':{'potion':2},'root':{'lead':'solo'}},note="ด่านบอสจะยากมากโดยไม่มีผู้ช่วย")],id='c_team')
say('raven',"รอบนี้ฉันนำแน่... แต่ถ้านายกล้านำก็ลองดู",'angry',id='t_lead',bg='guild_meeting')
say('karel',"สมัยฉัน... เอาเถอะ ฉันเป็นคนถือหอก นายเป็นคนสั่ง ฉันยอม",'smile')
go('t_lead2','pub')
say('karel',"สมัยฉัน ฉันก็ถูกนำแบบนี้ เข้าใจแล้ว ตามฉันมา เดินตรงกลาง อย่าเดินชิดผนัง",'normal',id='t_karel',bg='guild_meeting')
say('raven',"ห่า... ฉันไปเองก็ได้!",'angry')
go('t_karel2','pub')
say('horka',"ฮึ... กล้าหรือโง่ ยังไม่รู้ ถ้าตาย อย่าหวังให้ใครเก็บศพ",'normal',id='t_solo',bg='guild_master_room')
say('lola',"จดหมายด่วน! เซ็นรับด้วย ... อ๊ะ พี่จะไปคนเดียวเหรอคะ",'shock')

# ============ บทที่ 4: ผับหนวดปลาหมึกเมา ============
nar("คืนก่อนออกเดินทาง คุณแวะผับหนวดปลาหมึกเมา เสียงหัวเราะและกลิ่นเหล้าลอยอบอวล",id='pub',bg='guild_pub')
say('tobias',"ดื่มก่อน เดี๋ยวเล่าให้ฟัง ... มุมนั้น คนที่นั่งคนเดียว วาเลนซ์ เขานั่งตรงนั้นสามวันแล้ว ไม่ยอมแตะเหล้า",'normal')
say('vesper',"ข้อมูลแลกข้อมูล ถ้าเธอบอกฉันว่าเธอรู้อะไรเกี่ยวกับวาเลนซ์ ฉันจะบอกเรื่องที่เธอยังไม่รู้... เขากลับมาตอนฟ้าสาง ตัวเย็นเฉียบ เหมือนคนที่ควรตายไปแล้ว",'smile')
say('valenz',"ฉันไม่ได้ตายสักหน่อย...",'sad')
choice("วาเลนซ์เงยหน้ามองคุณ สายตาเหมือนคนไม่ได้นอนมานาน",[
 opt("ซื้อน้ำให้เขาแล้วนั่งลงเงียบๆ (ให้ความไว้ใจ)","v_trust",long=True,do={'root':{'valenz':'trusted'},'gas':-20},note="วาเลนซ์จะจำความใจดีนี้"),
 opt("ถามตรงๆ ว่าข้างล่างเกิดอะไรขึ้น","v_ask"),
 opt("แอบฟังเวสเปอร์ เธอพูดถูก เขาน่าสงสัย","v_sus",long=True,do={'root':{'valenz':'suspected'},'flag':['vesper_deal']},note="วาเลนซ์จะไม่ช่วยคุณอีก")],id='c_valenz')
say('valenz',"...ขอบใจ ไม่มีใครซื้ออะไรให้ฉันมานานแล้ว ฟังนะ ผู้พิทักษ์ข้างล่างไม่ได้ชั่วร้าย มันกลัวไฟ อย่ามองมันเป็นศัตรูทันที แล้วก็... อย่าเชื่อใจก็อบลินที่ยิ้ม",'sad',id='v_trust')
do_=dict(t='jump',cases=[],next='shop_hub',id='v_trust2');add(do_)
check('wit',12,"อ่านสีหน้าวาเลนซ์ว่าเขากำลังปิดบังอะไร",'v_ok','v_fail',id='v_ask')
say('valenz',"...เธอดูออกสินะ ข้างล่าง มีของที่ฉันเอามา... ขอโทษ ฉันบอกได้แค่ว่าผู้พิทักษ์แพ้ไฟ และคนงานยังมีชีวิตอยู่ที่ทะเลสาบ",'sad',id='v_ok',do={'flag':['known_weak_fire','miners_alive']})
go('v_ok2','shop_hub')
say('valenz',"ไม่มีอะไรจะพูด ไปเถอะ",'angry',id='v_fail')
go('v_fail2','shop_hub')
say('vesper',"ข้อมูลแลกข้อมูล ... เขามีของบางอย่างซ่อนอยู่ในเสื้อ ฉันเห็นมันเรืองแสงสีแดง ของแถม: เหมืองมี 'ผู้พิทักษ์' เกราะเหล็กตัวใหญ่ ขยับตอนมีคนเข้าใกล้ทะเลสาบ",'smile',id='v_sus',do={'flag':['known_guardian']})
go('v_sus2','shop_hub')

# ============ บทที่ 5: เตรียมของ ============
nar("ก่อนออกเดินทาง คุณมีเวลาเตรียมของที่ตลาดท่าเรือ",id='shop_hub',bg='harbor_market')
choice("จะไปร้านไหนก่อน?",[
 opt("ร้านช่างตีเหล็กบรอม (อาวุธ/เกราะ)","shop_brom"),
 opt("ร้านยาใบไม้ทอง (ยา/ของกิน)","shop_leaf"),
 opt("พอแล้ว ออกเดินทางไปประตูเมืองเหนือ","gate")],id='c_shop')
say('brom',"ของดีไม่ต้องเถียงราคา ดูเอาเอง",'normal',id='shop_brom',bg='brom_smithy')
shop(['sword_common','spear_common','dagger_common','axe_common','staff_common','wand_common','bow_common','sword_uncommon','spear_uncommon','staff_uncommon','robe_common','light_common','medium_common','shield_common'],'shop_hub',id='sh1',title="ร้านช่างตีเหล็กบรอม")
say('ferly',"อย่าดมขวดนั้นนะ! ... ยาฟื้นฟูกับของกิน เอาไปเลยจ้ะ",'smile',id='shop_leaf',bg='golden_leaf')
shop(['@potion','@bread','@antidote'],'shop_hub',id='sh2',title="ร้านยาใบไม้ทอง")

# ============ บทที่ 6: ประตูเมืองเหนือ ============
say('sissa',"ชื่อ ธุระ ปลายทาง",'normal',id='gate',bg='north_gate')
choice("กัปตันซิสซาจ้องคุณเขม็ง ใบอนุญาตอยู่ในมือคุณแล้ว",[
 opt("ตอบตรงๆ ตามความจริง","sis_true"),
 opt("อ้างว่าไปหาของป่าให้กิลด์ (โกหก)","sis_lie"),
 opt("ยื่นถุงเหรียญ 30 กัสให้ลับๆ","sis_bribe",do={'gas':-30,'flag':['bribed_sissa']})],id='c_gate')
say('sissa',"เหมืองใต้ภูผา... ดี ฉันไม่ถามต่อ ระวังตัว ฟังนะ ถ้าเห็นของแปลกที่ไหลมาจากเหมือง ส่งข่าวให้ฉันก่อนกิลด์",'normal',id='sis_true',do={'flag':['sissa_ally']})
go('sis_true2','road')
check('wit',11,"พูดโกหกให้แนบเนียนต่อหน้านักสืบ",'sis_lie_ok','sis_lie_fail',id='sis_lie')
nar("ซิสซาหรี่ตา แต่ยอมโบกมือให้ผ่าน",id='sis_lie_ok')
go('sis_lie_ok2','road')
say('sissa',"โกหกไม่เก่ง ฉันเห็นรอยโคลนเหมืองที่รองเท้าเธอ... ผ่านไปได้ แต่ฉันจำหน้าเธอแล้ว",'angry',id='sis_lie_fail',do={'flag':['sissa_suspicious']})
go('sis_lie_fail2','road')
say('sissa',"...ฉันไม่เห็นอะไรทั้งนั้น ไปเถอะ",'normal',id='sis_bribe')
go('sis_bribe2','road')

# ============ บทที่ 7: ถนนหลวงสู่เหมือง ============
nar("ถนนหลวงทอดยาวไปทางเหนือ ผ่านป่าชานเมืองและสะพานหินเก่า เด็กส่งของวิ่งสวนทางมา",id='road',bg='royal_road')
say('tib',"ส่งของค่ะ! ผมหมายถึงครับ! ... พี่ๆ จะไปเหมืองเหรอครับ ระวังนะครับ เมื่อเช้าผมเห็นก็อบลินหลายตัวแอบอยู่ตรงสะพาน",'shock')
nar("ที่สะพานหินเก่า เงาก็อบลินสอดแนมสองตัวโผล่ออกมาจากพุ่มไม้!",bg='old_stone_bridge')
battle(['goblin_scout'],'road_win','road_lose',id='b_road',ally='karel',intro="ก็อบลินสอดแนมขวางสะพาน",bg='old_stone_bridge')
say('karel',"ฮึ... พวกมันมาไกลกว่าที่คิด ก็อบลินไม่ควรโผล่แถวนี้ นี่มันผิดปกติ",'normal',id='road_win',do={'exp':40,'gasplus':15})
go('road_win2','village')
nar("คุณเข่าทรุด ขณะที่ทุกอย่างมืดลง... ก่อนสติจะหลุด คุณรู้สึกว่ามีคนลากคุณไปที่ปลอดภัย",id='road_lose',do={'heal':True,'flag':['rescued_by_tib']})
say('tib',"พี่ฟื้นแล้วเหรอครับ! ผมลากพี่ออกมาจากพุ่มไม้ ... อย่าบอกใครนะครับว่าผมวิ่งหนี!",'shy')
go('road_lose2','village')

# ============ บทที่ 8: หมู่บ้านคนขุดแร่ ============
nar("หมู่บ้านคนขุดแร่เงียบกริบ หน้าบ้านหลายหลังแขวนผ้าสีดำ",id='village',bg='miner_village')
say('win',"หมู่บ้านนี้อยู่ได้เพราะเหมือง... แต่ตอนนี้เหมืองกินลูกหลานเราไปเจ็ดคน หนึ่งในนั้นคือหลานชายฉัน ปิ๊ป อายุสิบหก",'sad')
say('orek',"ลงไปเหรอ ฉันไม่ไปด้วยนะ ... แต่ฉันมีของให้ แผนผังชั้นล่าง กับตราผนึกควบคุมผู้พิทักษ์ ถ้าเธอสัญญาข้อหนึ่ง",'normal')
choice("โอเรกหยิบตราโลหะสลักรูนออกมา \"สัญญาข้อไหน?\"",[
 opt("\"พาคนงานกลับมาให้ครบก่อน เรื่องอื่นทีหลัง\"","o_miners",long=True,do={'flag':['has_rune'],'root':{'orek':'miners_first'}},note="ผู้พิทักษ์อาจ 'สงบได้' ถ้าคุณใช้ตราถูกวิธี"),
 opt("\"ข้าขอค่าจ้างล่วงหน้า 200 กัส\"","o_pay",do={'gas':200,'flag':['has_rune'],'root':{'orek':'paid'}}),
 opt("\"ข้าสัญญาว่าจะทำลายผู้พิทักษ์ ให้เหมืองกลับมาใช้ได้\"","o_destroy",long=True,do={'flag':['has_rune'],'root':{'orek':'destroy_guardian'}},note="หมู่บ้านจะได้เหมืองคืน แต่ผู้พิทักษ์ปกป้องบางอย่างอยู่")],id='c_orek')
say('orek',"ดี... รูนบนตรานี่ใช้สั่งให้ผู้พิทักษ์หยุดได้ครั้งเดียว ต้องเอาให้ใกล้ก่อน",'normal',id='o_miners')
go('o_m2','camp')
say('orek',"โลภนะ... แต่ซื่อตรงดี เอาไป อย่าหนีล่ะ",'normal',id='o_pay')
go('o_p2','camp')
say('orek',"นั่นแหละที่ฉันอยากได้ยิน เจ้าไปจัดการมัน ฉันจะรอข่าว",'angry',id='o_destroy')

# ============ บทที่ 9: แคมป์ปากเหมือง ============
nar("ค่ำแล้ว ที่แคมป์ปากเหมือง ร่างสูงใหญ่ขวางทางเข้าไว้ เป็นซัน ยามผิวคล้ำร่างยักษ์",id='camp',bg='mine_camp')
say('sun',"ผ่านไปไม่ได้ จนกว่าจะรุ่งเช้า",'normal')
choice("คุณจะทำอย่างไร?",[
 opt("พักผ่อนจนเช้า (ฟื้น HP/MANA เต็ม)","s_rest",do={'heal':True}),
 opt("ลองโน้มน้าวซันให้เปิดทาง","s_talk"),
 opt("รอให้ซันเผลอแล้วลอดเข้าไป","s_sneak")],id='c_camp')
nar("คุณนอนข้างกองไฟ ฝันเห็นเสียงโซ่ลากอยู่ใต้ดิน เช้าวันใหม่ ซันเปิดทางให้พร้อมพยักหน้าสั้นๆ",id='s_rest')
go('s_rest2','floor1')
check('wit',12,"โน้มน้าวยามผู้ทำตามกฎอย่างเคร่งครัด",'s_talk_ok','s_talk_fail',id='s_talk')
say('sun',"...ก็ได้ เพราะเธอไม่ได้หนีเหมือนคนอื่น ผ่านไป",'smile',id='s_talk_ok')
go('s_talk_ok2','floor1')
say('sun',"ผ่านไม่ได้ กลับไปพักซะ",'angry',id='s_talk_fail',do={'heal':True})
go('s_talk_fail2','floor1')
check('spd',12,"เคลื่อนตัวเงียบๆ ผ่านยามยักษ์",'s_sneak_ok','s_sneak_fail',id='s_sneak')
nar("คุณลอดผ่านเงาของซันไปได้ ใจเต้นแรงตลอดทาง",id='s_sneak_ok')
go('s_sneak_ok2','floor1')
say('sun',"ผ่านไปไม่ได้!",'angry',id='s_sneak_fail')
nar("ซันจับคุณวางข้างกองไฟ \"พักก่อน\" ไม่ได้ลงโทษอะไรนอกจากเสียเวลา",do={'heal':True})
go('s_sneak_fail2','floor1')

# ============ ชั้น 1 ============
nar("ปากทางเข้าคลังใต้ภูผา ลมเย็นพัดออกมาพร้อมกลิ่นดินชื้นและเหล็กเก่า",id='floor1',bg='dungeon_entrance')
nar("ห้องโถงก็อบลิน เสียงหัวเราะแหลมเล็กดังก้องไปมา กองไฟกลางห้อง และก็อบลินสอดแนมสองตัวเดินวนอยู่",bg='goblin_hall')
choice("คุณจะเข้าไปอย่างไร?",[
 opt("บุกตรงๆ ชนกับพวกมัน","h_fight"),
 opt("ย่องเข้าไปหลังกองไฟ","h_sneak"),
 opt("ตะโกนเจรจา: \"ข้าไม่ได้มาเพื่อต่อสู้!\"","h_talk")],id='c_hall')
battle(['goblin_scout','goblin_scout'],'h_win','h_lose',id='h_fight',ally='karel',bg='goblin_hall')
check('spd',12,"ย่องผ่านสายตาก็อบลินสอดแนม",'h_sneak_ok','h_sneak_fail',id='h_sneak')
nar("คุณลอดผ่านหลังกองไฟ พร้อมเห็นกระเป๋าของก็อบลินเปิดอยู่ มียาขวดหนึ่งตกอยู่",id='h_sneak_ok',do={'item':{'potion':1}})
go('h_sneak_ok2','three')
nar("เท้าคุณเหยียบกิ่งไม้! ก็อบลินสองตัวหันขวับ!",id='h_sneak_fail')
battle(['goblin_scout','goblin_scout'],'h_win','h_lose',id='h_sneak_fail2',ally='karel',bg='goblin_hall')
check('wit',15,"พูดจาให้ก็อบลินที่ไม่เข้าใจภาษากลางเข้าใจ",'h_talk_ok','h_talk_fail',id='h_talk')
say('goblin_shaman',"เจ้าเป็นคนพูดกับพวกเรา... กรักจะ 'ปล่อย' คนข้างล่างเมื่อเจ้ามาหา เขาอยู่ห้องบอส ห้องสมบัติมีกับดัก ระวังพื้นกลางห้อง",'normal',id='h_talk_ok',do={'flag':['goblin_tip']})
go('h_talk_ok2','three')
nar("ก็อบลินไม่เข้าใจ... หรือไม่ฟัง พวกมันพุ่งเข้าใส่!",id='h_talk_fail')
go('h_talk_fail2','h_fight')
nar("ก็อบลินล้มลง กองสมบัติเล็กๆ ของพวกมันกระจายอยู่ใกล้กองไฟ",id='h_win',do={'exp':80,'gasplus':40})
go('h_win2','three')
nar("คุณล้มลง ก็อบลินยึดของบางส่วน แล้วปล่อยคุณทิ้งไว้ที่ปากเหมือง",id='h_lose',do={'heal':True,'gas':-30,'flag':['lost_to_goblins']})
go('h_lose2','three')

nar("ทางแยกสามทาง ทางซ้ายมีรอยตะปูบนพื้น ทางกลางมีเสียงน้ำหยด ทางขวามีแสงสีทองเลือนราง",id='three',bg='three_way')
choice("ไปทางไหนก่อน?",[
 opt("ซ้าย: ห้องกับดัก","trap"),
 opt("กลาง: ทะเลสาบใต้ดิน","lake"),
 opt("ขวา: ลงไปห้องบอสชั้น 1","boss1")],id='c_three')

nar("ห้องกับดักเต็มไปด้วยแผ่นหินที่มีรอยขีด พื้นกลางห้องมีเสียงกลวง",id='trap',bg='trap_room')
jump([('helped_grong','trap_grong'),('grong_hint','trap_grong')],'trap_free',id='trap_j')
nar("เสียงของลุงโกร่งดังก้องในหัว \"ถ้าเจอห้องที่พื้นเสียงกลวง อย่าเหยียบตรงกลาง\" คุณเดินเลียบผนัง ปลอดภัย!",id='trap_grong',do={'flag':['trap_safe']})
go('trap_g2','trap_loot')
check('luck',8,"เหยียบแผ่นหินโดยไม่รู้ว่าอันไหนคือกับดัก (ดวงล้วนๆ)",'trap_luck','trap_hurt',id='trap_free')
nar("โชคดี! คุณก้าวพลาดแล้วแผ่นหินแค่ส่งเสียงกึกกัก",id='trap_luck',do={'flag':['trap_safe']})
go('trap_l2','trap_loot')
nar("ลูกดอกพุ่งออกจากผนัง! คุณเสียเลือดนิดหน่อย ก่อนสังเกตเห็นกลไก",id='trap_hurt',do={'hp':-30,'flag':['trap_known']})
go('trap_h2','trap_loot')
choice("ที่ปลายห้องมีคันโยกเก่า และมีเชือกเหล็กพาดอยู่เหนือทางไปห้องสมบัติ",[
 opt("ดึงคันโยก ปลดกับดักทั้งห้อง","trap_pull",do={'flag':['trap_off']}),
 opt("ดัดแปลงกับดักให้ชี้ไปทางห้องบอส ล่อกรักมาเหยียบ","trap_set",long=True,do={'flag':['prep_trap'],'root':{'trap':'set_for_grak'}},note="กรักจะอ่อนลงก่อนสู้ แต่อาจกระทบคนที่ผ่านทางนี้"),
 opt("เก็บของที่เหลือแล้วออกไป","trap_leave")],id='trap_loot')
nar("คุณปลดกลไกได้ทั้งหมด เข้าห้องสมบัติได้โดยปลอดภัย",id='trap_pull')
go('trap_p2','treasure')
nar("คุณเปลี่ยนมุมลูกดอกและเสริมแผ่นหิน ให้ใครก็ตามที่ลงบันไดมาจากห้องบอสเหยียบแล้วเสียหลัก",id='trap_set')
go('trap_s2','treasure')
go('trap_leave','three')
nar("ห้องสมบัติ หีบไม้ผุๆ สองใบ ด้านในมีของจริง",id='treasure',bg='treasure_room',do={'gasplus':120,'item':{'potion':1},'flag':['treasure_taken']})
go('treasure2','three')

nar("ทะเลสาบใต้ดินสงบนิ่ง หินงอกหินย้อยส่องแสงฟ้าจางๆ ริมน้ำมีเสียงสะอื้นเบาๆ",id='lake',bg='underground_lake')
say('dorn',"ช่วยด้วย... ผมคือดอร์น คนงานเหมือง พวกเราถูกผู้พิทักษ์ 'เก็บ' ไว้ที่ชั้นสาม เขาไม่ได้ทำร้ายเรา แต่ก็อบลินกรักรุกเข้ามา เราซ่อนอยู่ที่นี่...",'sad')
choice("ดอร์นหนาวสั่น แผลที่ขามีรอยเขียว เขายื่นของบางอย่างมา",[
 opt("ให้ยาพาเขากลับไปปากเหมือง (เสียยา 1 ขวด)","d_help",long=True,do={'item':{'potion':-1},'flag':['dorn_saved'],'root':{'dorn':'saved'}},note="ดอร์นจะเล่าเรื่องในหมู่บ้านให้เสียงดี"),
 opt("ถามข้อมูลเรื่องผู้พิทักษ์ก่อน","d_info",do={'flag':['known_guardian','known_weak_fire']}),
 opt("ปลอบใจแล้วบอกให้รออยู่ตรงนี้","d_wait")],id='c_dorn')
nar("คุณฉีดยาให้ดอร์น แล้วพาเขาไปพักที่ปากทาง ก่อนกลับมา เขาให้ ขวดไฟ ที่ซ่อนไว้กับตัว",id='d_help',do={'item':{'fireflask':1}})
go('d_help2','three')
say('dorn',"ผู้พิทักษ์... ตัวมันเป็นเหล็ก แต่ใจมันคือเตาไฟ ใช้ไฟรบกวน มันจะช้าลง ผมมีขวดไฟนี้ ... เอาไป",'normal',id='d_info',do={'item':{'fireflask':1}})
go('d_info2','three')
nar("ดอร์นพยักหน้าแผ่วเบา \"ผมจะรอ\"",id='d_wait')
go('d_wait2','three')

nar("ห้องบอสชั้น 1 เต็มไปด้วยกลิ่นเหม็นสาบ กรัก หัวหน้าก็อบลินตัวใหญ่ยืนอยู่บนกองสมบัติ มือถือค้อนหิน",id='boss1',bg='boss_room_1')
say('grak',"มนุษย์! เจ้าฆ่าลูกน้องข้า! ข้าจะบดกระดูกเจ้าเป็นผง!",'normal')
battle(['grak'],'grak_win','grak_lose',id='b_grak',ally='karel',prep=['prep_trap','grong_hint','goblin_tip'],bg='boss_room_1',intro="กรัก เงื้อค้อนหิน!")
nar("กรักล้มลง หายใจรวยริน ค้อนหินหลุดมือ สัญลักษณ์บนหน้ากากของเขาแตก... ดูเหมือนมีบางอย่างควบคุมมันอยู่",id='grak_win',do={'exp':400,'gasplus':180})
choice("กรักมองคุณด้วยดวงตาที่เปลี่ยนไป ไม่ใช่ความดุร้ายอีกต่อไป",[
 opt("ไว้ชีวิตกรัก ขอให้พาก็อบลินที่เหลือออกจากเหมือง","grak_spare",long=True,do={'flag':['spared_grak'],'root':{'grak':'spared'}},note="ก็อบลินจะไม่เป็นศัตรูกับคุณอีก แต่หมู่บ้านอาจไม่พอใจ"),
 opt("จบชีวิตกรัก เพื่อความปลอดภัยของหมู่บ้าน","grak_kill",long=True,do={'flag':['killed_grak'],'root':{'grak':'killed'}},note="หมู่บ้านปลอดภัยกว่าเดิม แต่ก็อบลินจะแค้น"),
 opt("ไม่ตัดสินใจ ปล่อยให้คาเรลจัดการ","grak_karel")],id='c_grak')
say('grak',"เจ้า... ไม่ฆ่าข้า? ข้าถูก 'สิ่ง' นั่นสั่ง... ตอนเจ้ามา มันเงียบ ข้าจะพาพรรคพวกออกไป สาบานด้วยเลือดก็อบลิน",'sad',id='grak_spare')
go('grak_s2','floor2')
nar("คุณทำสิ่งที่ต้องทำ ความเงียบเข้าครอบงำห้อง",id='grak_kill')
go('grak_k2','floor2')
say('karel',"...ฉันจัดการเอง ไม่ต้องพูดอะไรมาก เดินต่อไป",'normal',id='grak_karel',do={'flag':['karel_decided'],'root':{'grak':'karel_handled'}})
go('grak_ka2','floor2')
nar("กรักล้มเหนือกองสมบัติ คุณปลุกสติขึ้นได้ในมุมห้อง ใครสักคนลากคุณออกมาและทิ้งยาไว้",id='grak_lose',do={'heal':True,'flag':['lost_to_grak']})
go('grak_l2','three')

# ============ ชั้น 2 ============
nar("บันไดหินเก่าพาลงสู่ชั้น 2 อุโมงค์ขุดแร่โบราณ ราวเหล็กเป็นสนิม เสียงเคาะโลหะดังไกลๆ ที่หัวบันไดมีมุมพักเล็กๆ คุณหยุดพักหายใจ (HP/MANA ฟื้นเต็ม)",id='floor2',bg='three_way',do={'heal':True})
choice("ทางแยกในอุโมงค์ชั้น 2 มีสามทาง",[
 opt("อุโมงค์ที่มีเสียงขุดเหมือง (ก็อบลินนักขุด)","f2_miner"),
 opt("ห้องที่มีเสียงสั่นของวิญญาณ (วิญญาณเหมือง)","f2_spirit"),
 opt("ถ้ำใยแมงมุมที่มีเงาไหวๆ","f2_spider")],id='c_f2')
battle(['goblin_miner'],'f2_win','f2_lose',id='f2_miner',ally='karel',bg='boss_room_1',intro="ก็อบลินนักขุดเงื้อพลั่วเหล็กใส่คุณ!")
say('mine_spirit',"คนที่ยังเป็น... มาที่นี่... ได้ยินเสียงเราไหม... ผู้พิทักษ์ไม่ได้บ้า... มันถูกดวงตะวันบังคับ",'sad',id='f2_spirit',bg='underground_lake')
choice("วิญญาณเหมืองพูดแผ่วเบา มองตรามนตร์ที่คุณถือ",[
 opt("ฟังต่อไปอย่างตั้งใจ (ได้ข้อมูล)","sp_listen",long=True,do={'flag':['spirit_truth','known_guardian'],'root':{'spirit':'listened'}},note="รู้ความจริงเรื่องผู้พิทักษ์"),
 opt("ปัดทิ้ง ไม่เชื่อสิ่งที่ตายไปแล้ว","sp_ignore",do={'root':{'spirit':'ignored'}}),
 opt("ถามหาเส้นทางที่ปลอดภัย","sp_path",do={'flag':['f2_shortcut']})],id='c_spirit')
say('mine_spirit',"...ตราผนึกของโอเรก ถ้าใช้ถูกที่ ผู้พิทักษ์จะนิ่ง แต่... เขาต้องการให้ใครบางคนยกโทษ... เมื่อมันตื่นขึ้นมา",'sad',id='sp_listen')
go('sp_l2','floor3')
nar("วิญญาณจางหายไปเงียบๆ",id='sp_ignore')
go('sp_i2','floor3')
say('mine_spirit',"ทางซ้ายเสมอ... ผนังเรียบคือเพื่อน",'normal',id='sp_path')
go('sp_p2','floor3')
battle(['cave_spider'],'f2_win','f2_lose',id='f2_spider',ally='karel',bg='boss_room_1',intro="แมงมุมถ้ำกระโดดจากเพดาน!")
nar("เสียงเงียบลง ของที่ตกจากศัตรูมีค่านิดหน่อย",id='f2_win',do={'exp':100,'gasplus':50})
go('f2_w2','floor3')
nar("คุณล้มลง คาเรลลากคุณหนีออกมาได้ทัน",id='f2_lose',do={'heal':True,'flag':['lost_f2']})
go('f2_l2','floor3')

# ============ ชั้น 3 ============
nar("ชั้น 3 เย็นเยียบ ภูตน้ำแข็งเล็กๆ ล่องลอยอยู่ ไกลออกไป โกเล็มหินเดินช้าๆ ตามกฎไร้ชีวิต คุณพบจุดพักที่คนงานเก่าทิ้งไว้ (HP/MANA ฟื้นเต็ม)",id='floor3',bg='underground_lake',do={'heal':True})
nar("ก่อนถึงห้องบอส ทางเดินเต็มไปด้วยเกราะเหล็กเก่าที่เป็นเศษซาก ... และเสียงหายใจดังขึ้นเมื่อคุณเข้าใกล้ห้อง")
check('wit',12,"สังเกตกลไกหลังประตูห้องผู้พิทักษ์ว่ามันไวต่อไฟหรือเสียง",'pre_ok','pre_fail',id='pre_boss',bg='boss_room_3')
nar("คุณเห็นรอยไหม้รอบผนัง ผู้พิทักษ์ไวต่อความร้อนสูงจริง!",id='pre_ok',do={'flag':['known_weak_fire']})
go('pre_ok2','boss3')
nar("ไม่เห็นอะไรเด่นชัด แต่ก็ได้ยินเสียงโลหะขยับ...",id='pre_fail')

nar("ห้องบอสชั้น 3 เกราะเหล็กขนาดใหญ่ยืนขวางกลางห้อง ดวงตาแดงจาง ๆ ลืมขึ้นมา ข้างหลังมันคือซากเศษเตาโบราณและกลุ่มคนงานหกคนที่กอดกันอยู่",id='boss3',bg='boss_room_3')
say('mine_guardian',"...ผู้บุกรุก... ผนึก... ถูกทำลาย... ปกป้อง... ปกป้อง...",'normal')
choice("คุณจะรับมือกับเกราะผู้พิทักษ์ผู้โศกเศร้านี้อย่างไร?",[
 opt("ใช้ตราผนึกของโอเรกสั่งให้สงบ (ต้องมีตรา)","mg_rune",long=True,do={'root':{'guardian':'calmed'}},note="ผู้พิทักษ์จะยังอยู่ปกป้องเหมืองต่อไป"),
 opt("ต่อสู้ ใช้ทุกอย่างที่เตรียมมา","mg_fight",long=True,do={'root':{'guardian':'fought'}},note="สู้ชนะ หมู่บ้านได้เหมืองคืน แต่ผู้พิทักษ์จะไม่กลับมา"),
 opt("ถอยก่อน กลับไปเตรียมตัวและมาใหม่","mg_back")],id='c_guard')
jump([('has_rune','mg_rune_ok')],'mg_rune_no',id='mg_rune')
nar("คุณชูตราโลหะรูนขึ้นเหนือหัว แสงสีฟ้าส่องสว่าง ผู้พิทักษ์หยุดนิ่ง ดวงตาแดงค่อยๆ เป็นสีขาว",id='mg_rune_ok')
say('mine_guardian',"...ตรา... ของ 'ผู้ดูแล'... ข้า... รู้แล้ว... ผู้ที่ขโมยเตาไฟ... คือคนที่ 'ตายแล้ว' ... แต่ยังเดินได้...",'sad')
go('mg_rune_ok2','valenz_reveal')
nar("คุณไม่มีตราผนึก ตรารูนที่ควรช่วยคุณอยู่ในมือโอเรกที่บนผิวดิน!",id='mg_rune_no')
go('mg_rune_no2','guard_fight')
go('mg_fight','guard_fight')
nar("เสียงเกราะเหล็กคำรามขึ้น... คุณถอยออกมาอย่างปลอดภัย มีเวลาเตรียมตัวอีกพักหนึ่ง",id='mg_back',do={'heal':True,'flag':['retreated_once']})
go('mg_back2','shop_late')
nar("คุณมีเวลาเตรียมของครั้งสุดท้าย (ใช้ของที่เหลือ/เงินที่หามาได้)",id='shop_late')
shop(['@potion','@fireflask','@antidote'],'boss3',id='sh3',title="ของที่พกมา (ซื้อจากคาเรล/ค้าขายลับ)")
battle(['mine_guardian'],'guard_win','guard_lose',id='guard_fight',ally='karel',prep=['known_weak_fire','spirit_truth','dorn_saved'],bg='boss_room_3',intro="ผู้พิทักษ์เหมืองเงื้อดาบเหล็กยักษ์!")
nar("เกราะผู้พิทักษ์ล้มลง เสียงโลหะดังก้อง... ภายในมีเปลวไฟดวงเล็กๆ ที่ค่อยๆ ดับ",id='guard_win',do={'exp':900,'gasplus':300,'flag':['killed_guardian']})
go('guard_w2','valenz_reveal')
nar("คุณล้มลง เกราะผู้พิทักษ์ไม่ได้ฆ่าคุณ เพียงแค่ผลักออกไปนอกห้อง และปิดประตู",id='guard_lose',do={'heal':True,'flag':['lost_to_guardian']})
go('guard_l2','shop_late')

# ============ ความจริง ============
nar("ในเงามืดหลังเตาไฟ มีใครบางคนยืนอยู่ นั่นคือ วาเลนซ์ ในมือถือก้อนอัญมณีสีเลือดที่เรืองแสง",id='valenz_reveal',bg='boss_room_3')
say('valenz',"...ฉันขโมย 'หัวใจเตา' ไปจากผู้พิทักษ์ หวังว่ามันจะรักษาคำสาปในตัวฉัน... แต่ผลคือผู้พิทักษ์บ้าคลั่ง ก็อบลินที่ถูกควบคุมบุกเข้ามา คนงานเลยติดอยู่ที่นี่",'sad')
jump([('valenz:trusted','vr_trust'),('valenz:suspected','vr_sus')],'vr_neutral',id='vr_j')
say('valenz',"เธอเป็นคนเดียวที่ซื้อน้ำให้ฉัน... ฉันขอโทษ เธอจะเอาหัวใจเตานี่ไปคืนก็ได้ หรือไม่ ฉันจะรับผิดเอง",'sad',id='vr_trust')
go('vr_t2','vr_choice')
say('valenz',"เธอเชื่อเวสเปอร์ ใช่ไหม... ก็ถูกแล้ว ฉันนี่แหละตัวการ",'angry',id='vr_sus')
go('vr_s2','vr_choice')
say('valenz',"นี่คือหัวใจเตา ฉันไม่รู้ว่าจะทำยังไงต่อ",'sad',id='vr_neutral')
choice("วาเลนซ์ยื่นก้อนอัญมณีหัวใจเตาให้คุณ ทุกคนมองมาที่คุณ",[
 opt("นำหัวใจเตาไปคืนผู้พิทักษ์ ปล่อยวาเลนซ์ไปตามทาง","vr_return",long=True,do={'flag':['returned_heart'],'root':{'valenz_end':'forgiven'}},note="ผู้พิทักษ์สงบ วาเลนซ์รอดจากการลงโทษ"),
 opt("จับวาเลนซ์ส่งกิลด์ ฮอร์ก้าตัดสินเอง","vr_arrest",long=True,do={'flag':['arrested_valenz'],'root':{'valenz_end':'arrested'}},note="วาเลนซ์จะถูกลงโทษตามกฎกิลด์"),
 opt("เก็บหัวใจเตาไว้เอง เป็นความลับระหว่างคุณกับวาเลนซ์","vr_keep",long=True,do={'flag':['kept_heart'],'root':{'valenz_end':'secret'}},note="ของมีพลังมหาศาลอยู่กับคุณ แต่ผู้พิทักษ์จะไม่ได้รับการเยียวยา")],id='vr_choice')
nar("หัวใจเตากลับเข้าที่ ไฟลุกขึ้นอีกครั้ง ผู้พิทักษ์ก้มศีรษะลงช้าๆ เหมือนจะขอบคุณ",id='vr_return')
go('vr_r2','epilogue')
say('valenz',"...ฉันยอมรับ พาฉันไปเถอะ",'sad',id='vr_arrest')
go('vr_a2','epilogue')
nar("หัวใจเตาอุ่นอยู่ในกระเป๋า ผู้พิทักษ์เงียบงัน",id='vr_keep')
go('vr_k2','epilogue')

# ============ บทส่งท้าย ============
nar("หลายวันต่อมา คุณพาคนงานที่เหลือขึ้นสู่ปากเหมือง เสียงร้องไห้ปนเสียงโห่ร้องดังทั่วหมู่บ้าน",id='epilogue',bg='miner_village')
say('win',"ปิ๊ป! หลานรัก...",'smile')
jump([('dorn_saved','ep_dorn')],'ep_loan',id='ep_j')
say('dorn',"ผมบอกทุกคนในหมู่บ้านแล้วว่าใครช่วยชีวิตพวกเรา",'smile',id='ep_dorn',do={'gasplus':100})
jump([('debt:big','ep_big'),('debt:small','ep_small')],'ep_mint',id='ep_loan')
say('linde',"ครบกำหนดแล้วค่ะ ยอดคืน 2,600 กัส... กำไรสุทธิ ไม่ใช่ยอดขาย",'normal',id='ep_big',do={'gas':-2600,'bg':'guild_counter'})
go('ep_b2','ep_mint')
say('linde',"ยอดคืน 600 กัส เรียบร้อยค่ะ",'smile',id='ep_small',do={'gas':-600,'bg':'guild_counter'})
go('ep_s2','ep_mint')
say('mint',"พี่กลับมาแล้ว!",'smile',id='ep_mint',bg='guild_lobby')
jump([('mint:promised','ep_mp'),('mint:tried','ep_mt')],'ep_mn',id='ep_mj')
say('mint',"พี่รักษาสัญญา! ขนมปังของหนูอยู่ไหนคะ?",'shock',id='ep_mp',do={'flag':['mint_loves_you']})
nar("คุณหยิบขนมปังจากร้านป้าแมกกี้ที่ซื้อมาจากตลาด ให้เธอด้วยรอยยิ้ม (หากไม่มีขนมปัง มิ้นท์จะเข้าใจ เพราะพี่รักษาสัญญาแล้ว)")
go('ep_mp2','ep_horka')
say('mint',"พี่พยายามจริงๆ ใช่ไหม... ขอบคุณค่ะ",'smile',id='ep_mt')
go('ep_mt2','ep_horka')
nar("มิ้นท์มองคุณเงียบๆ แล้วโบกมือเบาๆ",id='ep_mn')
say('horka',"ของกิลด์ ต้องกลับมาครบ... เจ้ากลับมาครบ ดี",'normal',id='ep_horka',bg='guild_master_room')
say('horka',"เจ้าเป็นนักผจญภัยของใบเรือเงินแล้วอย่างเป็นทางการ แต่ฟังไว้ เรื่องไม่จบแค่ใต้ภูผา ... ของที่ถูกขโมยไป มีมากกว่านี้ และบางอย่างกำลังกลับมา",'normal')
end("จบ Act 1: ใบเรือเงิน")
# ---- ลิงก์อัตโนมัติ ----
n=0
for i,x in enumerate(L):
    if not x.get('id'): n+=1; x['id']=f'n{n:03d}'
S={x['id']:x for x in L}
for i,x in enumerate(L):
    if x['t'] in('say','narr') and 'next' not in x: x['next']=L[i+1]['id']
for x in L:
    for k in ('goto','ok','fail','win','lose','next'):
        v=x.get(k)
        if v and v not in S: print('!! missing',x['id'],k,v)
    for o in x.get('opts',[]):
        if o['goto'] not in S: print('!! missing opt',x['id'],o['goto'])
    for c in x.get('cases',[]):
        if c[1] not in S: print('!! missing case',x['id'],c[1])
# แปลงเงื่อนไข jump
for x in L:
    for k in list(x):
        if x[k] is None: del x[k]

ROOTS={
 'mint':('คำสัญญาของมิ้นท์',{'promised':'สัญญาเต็มที่ว่าจะกลับมา','tried':'บอกว่าจะพยายามที่สุด','silent':'ลูบหัวโดยไม่ตอบ'}),
 'debt':('หนี้กิลด์',{'none':'ไม่กู้','small':'กู้ 500 (คืน 600)','big':'กู้ 2,000 (คืน 2,600)'}),
 'lead':('การนำทีม',{'self':'เป็นหัวหน้าเอง (ไรเวนเป็นคู่แข่ง)','karel':'ให้คาเรลนำ','solo':'ไปเดี่ยว'}),
 'valenz':('ท่าทีต่อวาเลนซ์',{'trusted':'ให้ความไว้ใจ','suspected':'สงสัยตามเวสเปอร์'}),
 'orek':('สัญญากับโอเรก',{'miners_first':'พาคนงานกลับก่อน','paid':'รับค่าจ้างล่วงหน้า','destroy_guardian':'สัญญาทำลายผู้พิทักษ์'}),
 'trap':('กับดักห้องที่ 2',{'set_for_grak':'ตั้งกับดักไว้ล่อกรัก'}),
 'dorn':('ดอร์น',{'saved':'ช่วยดอร์นไว้'}),
 'grak':('ชะตากรรมของกรัก',{'spared':'ไว้ชีวิต','killed':'สังหาร','karel_handled':'ปล่อยให้คาเรลจัดการ'}),
 'spirit':('วิญญาณเหมือง',{'listened':'ฟังความจริง','ignored':'ปัดทิ้ง'}),
 'guardian':('ผู้พิทักษ์',{'calmed':'ทำให้สงบ','fought':'ต่อสู้'}),
 'valenz_end':('บทสรุปของวาเลนซ์',{'forgiven':'ให้อภัย คืนหัวใจเตา','arrested':'ส่งตัวให้กิลด์','secret':'เก็บหัวใจเตาไว้เอง'}),
}
SPEAKERS={'dorn':'ดอร์น','grak':'กรัก','goblin_shaman':'ก็อบลินหมอผี','mine_guardian':'ผู้พิทักษ์เหมือง','mine_spirit':'วิญญาณเหมือง'}
json.dump({'title':'Act 1: ใบเรือเงิน','start':'start','roots':{k:{'label':v[0],'vals':v[1]} for k,v in ROOTS.items()},'speakers':SPEAKERS,'nodes':S},open('data/story/act1.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print(len(L),'nodes;',sum(1 for x in L if x['t']=='choice'),'choices;',sum(1 for x in L if x['t']=='choice' for o in x['opts'] if o.get('long')),'long-effect options')
