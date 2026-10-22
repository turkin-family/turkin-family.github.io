#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/thai_translations_court.py
Full Thai translation for the 17th Century Court Cases and Civil Service section (info-court-cases).
"""

def get_thai_court_html():
    return """    <!-- 17th CENTURY COURT BATTLES & STATE SERVICE SECTION (THAI) -->
    <div class="info-card" id="info-court-cases" style="border-left: 4px solid #b45309; background: linear-gradient(180deg, rgba(245, 158, 11, 0.03) 0%, var(--bg-surface) 100%);">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.75rem; margin-bottom:1rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <span style="font-size:2.2rem;">⚖️</span>
          <div>
            <h2 style="margin:0; font-size:1.35rem; color:var(--text-main);">การรับราชการแผ่นดินและคดีความแห่งตระกูลเตอร์คินในคริสต์ศตวรรษที่ 17</h2>
            <div style="font-size:0.84rem; color:var(--text-muted); margin-top:0.2rem;">ชุดเอกสารการสืบสวน บันทึกคำให้การต่อหน้าไม้กางเขน และหนังสือสั่งการราชการแห่งแขวงยาเรนสค์และสำนักพระสังฆราชโวล็อกดา (ค.ศ. 1646–1698)</div>
          </div>
        </div>
        <span style="background:#fffbeb; color:#b45309; font-weight:700; font-size:0.78rem; padding:0.35rem 0.8rem; border-radius:6px; border:1px solid #fde68a; box-shadow:0 1px 3px rgba(0,0,0,0.05);">หอจดหมายเหตุ GAVO • กองทุน 1260 «สำนักพระสังฆราชโวล็อกดา»</span>
      </div>

      <p style="font-size:0.92rem; line-height:1.65; color:var(--text-main); margin-bottom:1.25rem;">
        ชุดเอกสารคดีความและบันทึกการสืบสวนต้นฉบับศตวรรษที่ 17 จากหอจดหมายเหตุสำนักพระสังฆราชโวล็อกดา สะท้อนเรื่องราวชีวิตอันเข้มข้น ดุเดือด และยิ่งใหญ่ของบรรพบุรุษสายตรงของตระกูลเตอร์คิน ซึ่งแตกต่างจากสำมะโนสถิติแห้งแล้งทั่วไป เอกสารเหล่านี้บันทึกด้วยลายมือ скоропись (ภาษารัสเซียโบราณก่อนยุคพระเจ้าปีเตอร์) ถ่ายทอดคำให้การจากการสาบานจุมพิตไม้กางเขน คดีความแย่งชิงที่ดิน การค้าขายและสัญญากู้ยืมเงิน ตลอดจนการปฏิบัติหน้าที่ราชการแผ่นดินและภารกิจการทูตของตระกูลเตอร์คิน บนอาณาเขตกว้างใหญ่ไพศาลตั้งแต่กรุงมอสโก มหานครโวล็อกดา ข้ามเทือกเขาอูราลไปถึงเมืองซูร์กุตบนแม่น้ำอ็อบในไซบีเรีย และป้อมปราการปุสโตเซียร์สค์ในแดนอาร์กติก
      </p>

      <!-- GRID OF 9 CHRONICLE CASES -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(360px, 1fr)); gap:1.25rem;">

        <!-- CASE 1: 1646 (№ 633) AFANASY & VASILY -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1646 • เอกสาร скоропись 16 แผ่น</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 633</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              คดีข้อพิพาทเรื่องที่ดินและการปะทะ: คำร้องทุกข์ของบาทหลวงกัฟริอิล คอสโตรมิน ต่อนายสเตปัน เยฟีมเยฟ, อฟานาซี และ วาซีลี เตอร์คิน
            </h3>
            <div style="font-size:0.77rem; background:rgba(37,99,235,0.06); border-left:3px solid #2563eb; padding:0.4rem 0.6rem; border-radius:0 4px 4px 0; margin-bottom:0.6rem; color:var(--text-main); line-height:1.5;">
              <strong>⚖️ คู่ความในคดี:</strong>
              <div style="margin-top:0.25rem; padding-left:0.2rem; display:flex; flex-direction:column; gap:0.18rem;">
                <div>• <strong>โจทก์:</strong> บาทหลวงกัฟริอิล คอสโตรมิน เจ้าอาวาสวัดเวเดนสกายา</div>
                <div>• <strong>จำเลย:</strong> 1) นายสเตปัน เยฟีมเยฟ (เพื่อนบ้านผู้ครอบครองที่ดินวัด); 2) อฟานาซี เตอร์คิน และ วาซีลี เตอร์คิน (ผู้ดูแลอาณาเขตและวิวาทกับบาทหลวง)</div>
                <div>• <strong>ตุลาการ:</strong> พระอัครสังฆราชมาร์เคลล์แห่งโวล็อกดา</div>
              </div>
            </div>
            <div style="font-size:0.8rem; font-style:italic; background:var(--bg-surface); border:1px dashed #d9770666; padding:0.5rem 0.75rem; border-radius:6px; margin-bottom:0.65rem; color:#b45309; line-height:1.45;">
              «...ยื่นฟ้องเพื่อนบ้าน สเตปัน เยฟีมเยฟ ผู้เข้ายึดครองที่ดินของวัด และฟ้อง อฟานาซี กับ วาซีลี เตอร์คิน ผู้ด่าทอและวิวาททำร้าย...»
            </div>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              คดีสืบสวนประวัติศาสตร์ปี ค.ศ. 1646 ในปีเดียวกับการทำสำมะโนของอีวาน สเกรียบิน ซึ่งบันทึกไว้อย่างชัดเจนว่า อฟานาซี เป็น «ข้าราชการผู้แทนฝ่ายอาณาจักรของพระสังฆราช (Prikaznoy chelovek)». บาทหลวงกัฟริอิลแห่งวัดอ็อควัดได้ยื่นฎีกาต่อพระสังฆราชว่า อฟานาซีและวาซีลี เตอร์คิน เข้าข้างชาวบ้านในการปักปันเขตแดนที่ดิน และใช้อำนาจเข้าขัดขวางบาทหลวง
            </p>
            <div style="font-size:0.8rem; line-height:1.45; background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:0.45rem 0.65rem; border-radius:0 4px 4px 0; margin-bottom:0.75rem; color:var(--text-main);">
              <strong>💡 บทสรุปทางสาแหรก:</strong> เอกสารยืนยันสถานะที่แท้จริงของ อฟานาซี เซเมโนวิช เตอร์คิน ในฐานะข้าราชการปกครองสูงสุดของฝ่ายพระสังฆราชในแถบอ็อควัด ซึ่งเป็นฐานอำนาจและเศรษฐกิจที่ทำให้ทายาทรุ่นถัดมา (อีซาค และ บาทหลวงปีเตอร์) กลายเป็นผู้นำจิตวิญญาณแห่งลุ่มน้ำวิเชกดะ
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn active" onclick="openDocViewerById('gavo_1646_case633_afanasy_vasily_turkin')" style="font-size:0.74rem;">📜 เปิดดูเอกสารคดีในหอจดหมายเหตุ</button>
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
            <button class="pill-btn" onclick="focusPerson('I293'); switchTab('tree');" style="font-size:0.74rem;">🎯 วาซีลี</button>
          </div>
        </div>

        <!-- CASE 2: 1646 (№ 635) 75 RUBLES DEBT -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1646 • คดีพิจารณาหนี้สิน</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 635</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              หนี้สินส่วนกลางแห่งตำบล: การฟ้องร้องเรียกเงิน 75 รูเบิลเงินบริสุทธิ์โดยสมุหบัญชีปาลิตซิน
            </h3>
            <div style="font-size:0.77rem; background:rgba(37,99,235,0.06); border-left:3px solid #2563eb; padding:0.4rem 0.6rem; border-radius:0 4px 4px 0; margin-bottom:0.6rem; color:var(--text-main); line-height:1.5;">
              <strong>⚖️ คู่ความในคดี:</strong>
              <div style="margin-top:0.25rem; padding-left:0.2rem; display:flex; flex-direction:column; gap:0.18rem;">
                <div>• <strong>โจทก์:</strong> สมุหบัญชี อันเดรย์ ปาลิตซิน</div>
                <div>• <strong>จำเลย:</strong> อฟานาซี เตอร์คิน, โอปารา อิวานอฟ, คอซมา โปโนมาเรฟ และตัวแทนชาวบ้านอุสต์-วิมและอ็อควัด</div>
                <div>• <strong>ตุลาการ:</strong> พระอัครสังฆราชมาร์เคลล์แห่งโวล็อกดา</div>
              </div>
            </div>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              เงิน 75 รูเบิลในศตวรรษที่ 17 ถือเป็นเงินจำนวนมหาศาล (เทียบเท่าม้าศึกพันธุ์ดี 75 ตัว หรือบ้านเรือนไม้ขนาดใหญ่ 15 หลัง). อฟานาซี เตอร์คิน ในฐานะตัวแทนชุมชน ได้เข้าต่อสู้คดีในศาลพระสังฆราชเพื่อปกป้องเงินกองกลางของชาวบ้านจากการเรียกเก็บเกินขนาดของเจ้าพนักงานส่วนกลาง
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
          </div>
        </div>

        <!-- CASE 3: 1656 SURGUT ODYSSEY 347 RUBLES -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1656 • ซูร์กุต — โวล็อกดา</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260 / เอกสารสถาบันประวัติศาสตร์ SPbII RAS</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              มหากาพย์ซูร์กุต (Surgut Odyssey) ของอาร์คิป เตอร์คิน: การค้าขนเฟอร์เซเบิลในไซบีเรียและหนี้สินผูกพัน 347 รูเบิล
            </h3>
            <div style="font-size:0.77rem; background:rgba(37,99,235,0.06); border-left:3px solid #2563eb; padding:0.4rem 0.6rem; border-radius:0 4px 4px 0; margin-bottom:0.6rem; color:var(--text-main); line-height:1.5;">
              <strong>⚖️ คู่ความในคดี:</strong>
              <div style="margin-top:0.25rem; padding-left:0.2rem; display:flex; flex-direction:column; gap:0.18rem;">
                <div>• <strong>โจทก์:</strong> อาร์คิป อฟานาซีเยวิช เตอร์คิน</div>
                <div>• <strong>จำเลย:</strong> อฟานาซี เซเมโนวิช เตอร์คิน (บิดา)</div>
                <div>• <strong>ตุลาการ:</strong> พระอัครสังฆราชมาร์เคลล์แห่งโวล็อกดาและเวลีโคเปียร์ม</div>
              </div>
            </div>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              เรื่องราวการเดินทางอันทรหดข้ามเทือกเขาอูราลสู่ไซบีเรียตอนเหนือ อาร์คิป เตอร์คิน ได้เดินทางไปค้าขายขนสัตว์มีค่า ณ เมืองซูร์กุตริมแม่น้ำอ็อบ และเข้าผูกพันสัญญากู้ยืมเงินก้อนใหญ่ถึง 347 รูเบิล เมื่อกลับมายังบ้านเกิด เกิดข้อพิพาทในครอบครัวเกี่ยวกับการชำระหนี้และการแบ่งมรดกที่ดิน
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
            <button class="pill-btn" onclick="focusPerson('I294'); switchTab('tree');" style="font-size:0.74rem;">🎯 อาร์คิป</button>
          </div>
        </div>

        <!-- CASE 4: 1656-1664 (№ 2347) OTPUSK & DOPROS -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1656–1664 • การแบ่งมรดกและสอบสวน</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 2347</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              «ขอยกโทษให้ทั้งสิ้น»: หนังสือแบ่งสรรทรัพย์สินและการที่อาร์คิปปฏิเสธเลี้ยงดูบิดา
            </h3>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              บันทึกคำให้การอันสะเทือนใจ อฟานาซีผู้ชราภาพได้ตกลงแบ่งทรัพย์สินให้แก่อาร์คิปบุตรชาย โดยมีเงื่อนไขให้อาร์คิปเลี้ยงดูบิดาจนสิ้นอายุขัย แต่อาร์คิปกลับไม่ปฏิบัติตามสัญญา นำไปสู่การไต่สวนต่อหน้าเจ้าคณะปกครองฝ่ายสงฆ์อุสต์-วิม
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
            <button class="pill-btn" onclick="focusPerson('I294'); switchTab('tree');" style="font-size:0.74rem;">🎯 อาร์คิป</button>
          </div>
        </div>

        <!-- CASE 5: 1667 (№ 2913) AFANASY VS ARKHIP & ISAAK -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1667 • เอกสารคดี 11 แผ่น</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 2913</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              ฎีกาของอฟานาซี ผู้เฒ่าแห่งตระกูล: ข้อร้องเรียนต่อนางเฟียกลา ซุซกินา (เรื่องที่ดิน) และต่อบุตรชาย อาร์คิป และ อีซาค (เรื่องการไม่ยอมเลี้ยงดูบิดา)
            </h3>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              อฟานาซีในวัยเกือบ 70 ปี ได้เดินทางเข้าสู่นครโวล็อกดาเพื่อยื่นฎีกาต่อพระสังฆราชซีโมน เพื่อทวงคืนสิทธิ์ในบ้านและที่ดินทำกินของตน คดีนี้เป็นหลักฐานชิ้นเอกที่บันทึกชื่อบุตรชายทั้งสองคนคือ อาร์คิป และ อีซาค ไว้อย่างครบถ้วนสมบูรณ์
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
            <button class="pill-btn" onclick="focusPerson('I295'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีซาค</button>
          </div>
        </div>

        <!-- CASE 6: 1678 (№ 5032) KIRILL TURKIN & BOYAR MATVEEV -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1677–1678 • ประวัติศาสตร์ร่วมระดับชาติ</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, คดี 4829, 5032</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              ราชการแผ่นดิน: การควบคุมตัวและคุ้มกันมหาเสนาบดี เจ้าพระยาบอยาร์ อาร์ตามอน มัตเวเยฟ สู่ป้อมปุสโตเซียร์สค์ โดยเจ้าพนักงานคิริลล์ เตอร์คิน
            </h3>
            <div style="font-size:0.77rem; background:rgba(37,99,235,0.06); border-left:3px solid #2563eb; padding:0.4rem 0.6rem; border-radius:0 4px 4px 0; margin-bottom:0.6rem; color:var(--text-main); line-height:1.5;">
              <strong>⚖️ เจ้าหน้าที่และผู้ร่วมภารกิจ:</strong>
              <div style="margin-top:0.25rem; padding-left:0.2rem; display:flex; flex-direction:column; gap:0.18rem;">
                <div>• <strong>เจ้าพนักงานตุลาการท้องถิ่น (Zemsky tselovalnik):</strong> คิริลล์ อฟานาซีเยวิช เตอร์คิน</div>
                <div>• <strong>นักโทษการเมืองชั้นสูง:</strong> «มหาเสนาบดีแห่งซาร์» เจ้าพระยาบอยาร์ อาร์ตามอน มัตเวเยฟ และบุตรชาย อันเดรย์</div>
                <div>• <strong>หัวหน้ากองคุ้มกัน:</strong> สโตลนิก กัฟริอิล ตูคาเชฟสกี</div>
              </div>
            </div>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              ภารกิจระดับชาติอันยิ่งใหญ่ในรัชสมัยซาร์เฟโอดอร์ อะเลคเซเยวิช เจ้าพระยาบอยาร์มัตเวเยฟ (อัครมหาเสนาบดีในรัชกาลก่อนและพระบิดาบุญธรรมของพระนางนาตาลยา นารึชกินา พระราชมารดาของพระเจ้าปีเตอร์มหาราช) ถูกเนรเทศไปยังป้อมปราการปุสโตเซียร์สค์ในแดนอาร์กติก คิริลล์ เตอร์คิน ได้รับแต่งตั้งให้เป็นเจ้าหน้าที่ทางการในการจัดหาเรือ เสบียง และควบคุมความสงบตลอดเส้นทางผ่านลุ่มแม่น้ำวิมและเปโชรา
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 สาแหรกเตอร์คิน</button>
          </div>
        </div>

        <!-- CASE 7: 1679 (№ 5260) ISAAK POSYLSHCHIK TO MOSCOW -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1679 • กรุงมอสโก, ทบวงคลังหลวง</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 5260</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              ภารกิจสู่กรุงมอสโก: นายอีซาค เตอร์คิน ผู้แทนนำส่งภาษีการศึกสงครามจาก 144 ครัวเรือน
            </h3>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              ในระหว่างสงครามรัสเซีย-ตุรกี (ค.ศ. 1676–1681) ทางการได้ระดมเงินภาษีการศึกเพื่อสนับสนุนกองทัพ อีซาค เตอร์คิน ได้รับความไว้วางใจให้เป็นผู้นำส่งเงินส่วยอากรจาก 144 ครัวเรือนในเขตลุ่มน้ำวิม เดินทางฝ่าพงไพรนับพันกิโลเมตรเข้าสู่กรุงมอสโก และส่งมอบต่อสมุหบัญชีหลวงแห่งวังหลวงมอสโกอย่างปลอดภัย
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I295'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีซาค</button>
          </div>
        </div>

        <!-- CASE 8: 1687-1688 (№ 7519) PRIEST PETR IN MOSCOW PODVORIE -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1687–1688 • ตำหนักผู้แทนพระสังฆราช ณ มอสโก</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, ทะเบียน 1, คดี 7519</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              ตำหนักผู้แทนพระสังฆราชในกรุงมอสโก: บาทหลวงปีเตอร์ เตอร์คิน ในการว่าความพิทักษ์ที่ดินตำบลปะทะสังฆมณฑลเวลีโคอุสติยูก
            </h3>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              ข้อพิพาททางศาสนจักรครั้งใหญ่ระหว่างสังฆมณฑลโวล็อกดากับสังฆมณฑลเวลีโคอุสติยูก บาทหลวงปีเตอร์ เตอร์คิน ได้รับมอบหมายให้พำนัก ณ ตำหนักผู้แทนพระสังฆราชในกรุงมอสโก เพื่อว่าความต่อหน้าคณะตุลาการสงฆ์แห่งพระสังฆราชใหญ่แห่งออลรัสเซียในการพิทักษ์สิทธิ์ที่ดินของชาวบ้าน
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I175'); switchTab('tree');" style="font-size:0.74rem;">🎯 สาแหรกเตอร์คิน</button>
          </div>
        </div>

        <!-- CASE 9: 1688-1698 (№ 7753, 8267, 10789) ISAAK VYBORNY SUDYA -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.4rem;">
              <span style="font-size:0.75rem; font-weight:700; background:#fef3c7; color:#b45309; padding:0.15rem 0.5rem; border-radius:4px; border:1px solid #fde68a;">ค.ศ. 1688–1698 • ศาลแขวงอุสต์-วิม</span>
              <span style="font-size:0.73rem; color:var(--text-muted);">GAVO ฟ. 1260, คดี 7753, 8267, 10789</span>
            </div>
            <h3 style="margin:0 0 0.5rem 0; font-size:1.02rem; color:var(--text-main); font-weight:700; line-height:1.35;">
              ผู้พิพากษาแห่งแขวงอุสต์-วิม: ทศวรรษแห่งอำนาจตุลาการของอีซาค เตอร์คิน
            </h3>
            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              ตลอดระยะเวลากว่า 10 ปี อีซาค อฟานาซีเยวิช เตอร์คิน ได้รับเลือกตั้งจากราษฎรทุกหมู่บ้านให้ดำรงตำแหน่งผู้พิพากษาท้องถิ่น (Vyborny sudya) ทำหน้าที่ตัดสินคดีความ มรดก ที่ดิน และสัญญาทางการค้าของชุมชน เป็นหลักฐานยืนยันถึงเกียรติยศและบารมีอันสูงส่งของตระกูลเตอร์คินในสังคมยุคโบราณ
            </p>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.4rem; border-top:1px dashed var(--border-color); padding-top:0.6rem;">
            <button class="pill-btn" onclick="focusPerson('I295'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีซาค</button>
          </div>
        </div>

      </div>
    </div>"""
