#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/thai_translations_clergy.py
Full Thai translation for the Orthodox Clergy and Parish Churches section (info-clergy).
"""

def get_thai_clergy_html():
    return """    <!-- ORTHODOX CLERGY & PARISH CHURCHES SECTION (THAI) -->
    <div class="info-card" id="info-clergy">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:1.6rem;">⛪</span>
        <h2 style="margin:0;">คณะสงฆ์ออร์โธดอกซ์และศาสนสถานของบรรพบุรุษ (คริสต์ศตวรรษที่ 17–20, ค.ศ. 1646–1937)</h2>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.2rem; line-height:1.6;">
        ตลอดเวลากว่า 300 ปี — ตั้งแต่ทะเบียนราษฎร์ศตวรรษที่ 17 จนถึงศตวรรษที่ 20 — จิตวิญญาณและวิถีชีวิตของบรรพชนทุกชั่วคนผูกพันแนบแน่นกับอารามหลวงและวัดประจำตำบลในแขวงยาเรนสค์, อุสต์-วิม และอุสต์-ซีโซลสค์ แห่งมณฑลโวล็อกดา (ปัจจุบันคือสาธารณรัฐโคมิและแคว้นคิรอฟ). ตระกูลเตอร์คินได้ให้กำเนิดวงศ์วานสงฆ์ชั้นสูง ไวยาวัจกร และนักบวชอารามหลวง ขณะที่ทุกสายตระกูลร่วมสาแหรก (ชุกโตมอฟ, ซิโนเวียฟ, ซูตคิน, โปเลชชิคอฟ, ปาซินคอฟ, คิซยูรอฟ, เลทอฟ, ยารานอฟ) ล้วนประกอบพิธีศีลจุ่ม ศีลสมรส และพิธีปลงศพ ณ อารามศักดิ์สิทธิ์เหล่านี้
      </p>

      <!-- STATS BANNER -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:0.75rem; margin-bottom:1.35rem;">
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#2563eb;">เกือบ 300 ปี</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">แห่งการรับใช้ศาสนาและพิทักษ์ศรัทธา (1646–1937)</div>
        </div>
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#7c3aed;">12+ อารามและวัด</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">โคควิทซี, ลัลสค์, คัดนิคอฟ, โวล็อกดา, อูลยานอโว, อึบ, ลอยมา, อุสต์-วิม, ลยาลี, อ็อควัด, ปาเลวิทซี, ยาเรนสค์</div>
        </div>
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#0284c7;">30+ นักบวชและผู้รับใช้</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">บาทหลวง, สังฆานุกร, ภิกษุอาราม, ผู้ช่วยพิธีกรรม และเจ้าหน้าที่ศาสนจักร</div>
        </div>
      </div>

      <!-- CHURCHES SUMMARY GRID WITH PHOTOS -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.15rem;">
        
        <!-- 1. КОКВИЦЫ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#2563eb;">🏛️ หมู่บ้านโคควิทซี — วัดพระคริสตสมภพ</h3>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bfdbfe;">ศูนย์กลางจิตวิญญาณตระกูล (150+ ปี)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เนินเขาโคควิทสกายา โกรา, แขวงยาเรนสค์ • ชุมชนตระกูล: เตอร์คิน, เลทอฟ, ยารานอฟ, ซิเซฟ</div>
            
            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png', 'Христорождественская церковь в с. Коквицы', 'Исповедная роспись 1773 г., двор 167 священника о. Степана Туркина')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png" alt="ทะเบียนวัดโคควิทซี 1773" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🏛️ วัดหินสองชั้นอันสง่างาม สร้างขึ้นในปี ค.ศ. 1795 แทนวัดไม้เดิม เป็นศูนย์รวมใจของชาวเนินเขาโคควิทซี 20 หมู่บ้าน</div>
                <div style="margin-top:0.35rem;">📜 บันทึกสำมะโนนักบวชปี ค.ศ. 1773 ยืนยันว่า บาทหลวงสเตฟาน ยาคอฟเลวิช เตอร์คิน และสังฆานุกร ดมิทรี อะเลคเซเยวิช เตอร์คิน เป็นผู้นำคณะสงฆ์ประจำวัดนี้</div>
              </div>
            </div>

            <p style="font-size:0.83rem; line-height:1.55; margin-bottom:0.65rem;">
              นักบวชในสายตระกูลที่รับใช้ ณ วัดพระคริสตสมภพแห่งนี้:
            </p>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>บาทหลวง สเตฟาน ยาคอฟเลวิช เตอร์คิน</strong> (1705–1782) — เจ้าอาวาสวัดพระคริสตสมภพยาวนานกว่า 40 ปี (คุณทวด 7 ชั่วคน)</li>
              <li><strong>สังฆานุกร ดมิทรี อะเลคเซเยวิช เตอร์คิน</strong> (1734–1799) — สังฆานุกรประจำวัด (คุณทวด 6 ชั่วคน)</li>
              <li><strong>ผู้ช่วยพิธีกรรม อะเลคซี สเตฟาโนวิช เตอร์คิน</strong> (1743–1805) — สังกัดคณะสงฆ์วัดโคควิทซี</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I175'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงสเตฟาน</button>
            <button class="pill-btn" onclick="focusPerson('I176'); switchTab('tree');" style="font-size:0.74rem;">🎯 สังฆานุกรดมิทรี</button>
          </div>
        </div>

        <!-- 2. ЛАЛЬСК -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #7c3aed33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#7c3aed;">⛪ เมืองลัลสค์ — มหาวิหารพระคืนชนม์</h3>
              <span style="background:#f5f3ff; color:#7c3aed; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #ddd6fe;">สังฆานุกรประจำมหาวิหาร (1870–1904)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เมืองการค้าโบราณลัลสค์ ริมแม่น้ำลูซา • แขวงเวลีโคอุสติยูก</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Лальск_Воскресенский_собор.jpg', 'Воскресенский собор в г. Лальске', 'Каменный собор 1717 г. постройки • Место служения соборного диакона о. Михаила Алексеевича Туркина (1870–1904 гг.)')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="фото_храмов/Лальск_Воскресенский_собор.jpg" alt="มหาวิหารลัลสค์" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🏛️ มหาวิหารหินศิลปะบาโรกโบราณ สร้างขึ้นในปี ค.ศ. 1717 เป็นศูนย์กลางศาสนาอันยิ่งใหญ่แห่งเมืองวาณิชลัลสค์</div>
                <div style="margin-top:0.35rem;">📜 สังฆานุกรประจำมหาวิหาร บาทหลวงมิคาอิล อะเลคเซเยวิช เตอร์คิน รับใช้ ณ แท่นบูชานี้อย่างซื่อสัตย์ยาวนานกว่า 34 ปี (ค.ศ. 1870–1904)</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>สังฆานุกร มิคาอิล อะเลคเซเยวิช เตอร์คิน</strong> (1838–1904) — สังฆานุกรอาวุโสแห่งมหาวิหารลัลสค์ ได้รับพระราชทานเหรียญเกียรติยศและเสื้อคลุมทองคำ</li>
              <li>สมรสกับ มาเรีย โปรโคเปียฟนา บรึซกาโลวา ธิดาตระกูลคหบดีใหญ่แห่งเมืองโซลวิเชกอดสค์</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I236'); switchTab('tree');" style="font-size:0.74rem;">🎯 สังฆานุกรมิคาอิล</button>
          </div>
        </div>

        <!-- 3. КАДНИКОВ, ВОЛОГДА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #9333ea33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#9333ea;">⛪ คัดนิคอฟ, โวล็อกดา, เกรียโซเวทส์ — แขวงศาสนจักรของบาทหลวงโปรโคปี</h3>
              <span style="background:#faf5ff; color:#9333ea; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #e9d5ff;">บาทหลวงประจำตำบล (1891–1915+)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">มณฑลโวล็อกดาตอนกลาง • ค.ศ. 1891–1915+</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Брусничное_Спасо_Преображенская_церковь.jpg', 'с. Спасское — Спасо-Преображенская церковь', 'Храм построения 1869–1884 гг. • Приход священника о. Прокопия Туркина')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="фото_храмов/Брусничное_Спасо_Преображенская_церковь.jpg" alt="วัดบรูสนิชโนเย" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🏛️ วัดการแปรสภาพของพระเยซูเจ้าบนเขาตาบอร์ ณ บรูสนิชโนเย (Spaso-Preobrazhenskaya) สร้างด้วยหินอันสง่างาม ค.ศ. 1869–1884</div>
                <div style="margin-top:0.35rem;">📜 บาทหลวงโปรโคปี มิคาอิโลวิช เตอร์คิน (บุตรสังฆานุกรมิคาอิลแห่งลัลสค์) สำเร็จการศึกษาจากวิทยาลัยศาสนศาสตร์โวล็อกดา และรับใช้เป็นเจ้าอาวาสประจำวัดนี้นานกว่า 14 ปี</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>บาทหลวง โปรโคปี มิคาอิโลวิช เตอร์คิน</strong> (เกิด 1868) — เจ้าอาวาสวัดปุสโตรัมยานสกายา นิโคลาเยฟสกายา และวัดสปัสสกายา</li>
              <li>อุทิศตนเพื่อการศึกษาของเด็กในชนบทและได้รับรางวัลยกย่องจากสังฆมณฑลโวล็อกดา</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I260'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงโปรโคปี</button>
          </div>
        </div>

        <!-- 4. УЛЬЯНОВО И КУЖБА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #4f46e533; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#4f46e5;">⛪ с. Ульяново и с. Кужба — อารามหลวงตรีเอกภาพเซนต์สเตฟาน</h3>
              <span style="background:#eef2ff; color:#4f46e5; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #c7d2fe;">ผู้สละชีพเพื่อศรัทธา ศตวรรษที่ 20</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">แขวงอุสต์-ซีโซลสค์และอุสต์-คุลอม • ลุ่มแม่น้ำวิเชกดะตอนบน • ค.ศ. 1865–1937</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Ульяново_Троице_Стефановский_монастырь.jpg', 'с. Ульяново — Троице-Стефановский мужской монастырь', 'อารามหลวงเซนต์สเตฟานแห่งเปียร์ม • วีรกรรมแห่งศรัทธาของพระภิกษุวิตาลี (เตอร์คิน), ค.ศ. 1937')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="фото_храмов/Ульяново_Троице_Стефановский_монастырь.jpg" alt="อารามหลวงอูลยานอโว" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🌲 อารามหลวงฝ่ายชายอันเลื่องชื่อแห่งแดนเหนือ ก่อตั้งโดยนักบุญสเตฟานแห่งเปียร์ม ปลายศตวรรษที่ 14 และฟื้นฟูขึ้นในศตวรรษที่ 19</div>
                <div style="margin-top:0.35rem;">⚖️ สำนวนคดีสืบสวนประวัติศาสตร์ UNKVD โคมิ ASSR ปี 1937 (หอจดหมายเหตุ FSB หมายเลข KP-7444)</div>
              </div>
            </div>

            <!-- พระภิกษุวิตาลี เตอร์คิน -->
            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.65rem 0; padding-left:1.15rem;">
              <li><strong>พระภิกษุ วิตาลี (วิตาลี อิวาโนวิช เตอร์คิน)</strong> (1865, หมู่บ้านโคควิทซี – 06.11.1937) — <strong>น้องชายแท้ๆ ของเทียด อะเลคซี อิวาโนวิช เตอร์คิน</strong> และเป็น <strong>คุณลุงแท้ๆ ของคุณทวด นิโคไล อะเลคเซเยวิช เตอร์คิน</strong> ท่านอุปสมบทเป็นพระภิกษุแห่งอารามหลวงอูลยานอฟสกี ภายหลังอารามถูกสั่งปิดในปี 1923 ท่านได้ย้ายไปจำพรรษา ณ หมู่บ้านคุจบะ พำนักในเรือนหลังเดียวกันกับ <strong>พระไอเอโรมอนัค เมเลตี (เฟดิวเนียฟ)</strong> พระเหรัญญิกของอาราม ร่วมกันประกอบพิธีกรรมทางศาสนาอย่างลับๆ ให้แก่ชาวบ้านนานถึง 14 ปี จนกระทั่งถูกจับกุมในเดือนกันยายน 1937 ถูกตัดสินจำคุกค่ายกักกันแรงงาน 10 ปี และมรณภาพ ณ ค่ายกักกันวอกวาซดีโน (ค่ายอุกต์เปชลาก) เมื่อวันที่ 6 พ.ย. 1937 (ได้รับการล้างมลทินกอบกู้เกียรติยศแล้ว)</li>
            </ul>

            <!-- ВЫДЕЛЕННЫЙ БЛОК: НОВОМУЧЕНИК МЕЛЕТИЙ -->
            <div style="background:linear-gradient(135deg, rgba(124,58,237,0.06), rgba(217,119,6,0.06)); border:1.5px solid rgba(124,58,237,0.25); border-radius:8px; padding:0.65rem 0.75rem; margin-bottom:0.75rem; display:flex; gap:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg', 'Преподобномученик МЕЛЕТИЙ иеромонах', 'พระเหรัญญิกอารามหลวง ผู้ร่วมคดีความปี 1937 เดียวกันกับพระภิกษุวิตาลี เตอร์คิน')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex:0 0 92px; text-align:center;">
                <img src="архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg" alt="พระมรณสักขี เมเลตี" style="width:92px; height:118px; object-fit:cover; border-radius:6px; border:1.5px solid #7c3aed; box-shadow:0 2px 5px rgba(0,0,0,0.15); display:block; transition:transform 0.2s; margin:0 auto;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'" />
                <div style="font-size:0.64rem; font-weight:700; color:#6d28d9; margin-top:0.35rem; width:100%; line-height:1.2;">นักบุญเมเลตี<br><span style="font-size:0.60rem; font-weight:600; color:var(--text-muted);">(เฟดิวเนียฟ)</span></div>
              </div>
              <div style="font-size:0.79rem; line-height:1.5; color:var(--text-main);">
                <div style="font-weight:700; color:#6d28d9; margin-bottom:0.2rem; font-size:0.82rem;">🕊️ การสถาปนาเป็นนักบุญของสหายร่วมคดีปี 1937:</div>
                <p style="margin:0 0 0.35rem 0; font-size:0.77rem; line-height:1.45; color:var(--text-main);">
                  <em>«มหาเถรสมาคมแห่งศาสนจักรออร์โธดอกซ์รัสเซีย มีมติลงวันที่ 6 ต.ค. 2001 ประกาศสถาปนาพระไอเอโรมอนัค เมเลตี (เฟดิวเนียฟ) ขึ้นเป็นนักบุญในหมู่นักบุญมรณสักขีและผู้ยืนหยัดแห่งรัสเซียในศตวรรษที่ 20»</em>
                </p>
                <div style="font-size:0.75rem; line-height:1.45; color:var(--text-main);">
                  • พระเหรัญญิกอารามหลวงอูลยานอฟสกี, <strong>ผู้ต้องหาในสำนวนคดีสืบสวนปี 1937 เดียวกันกับพระภิกษุวิตาลี เตอร์คิน</strong><br>
                  • ในปี ค.ศ. 1923–1937 ท่านทั้งสองได้อาศัยอยู่ร่วมกันในเรือนหลังเดียวกัน ณ หมู่บ้านคุจบะ ทำพิธีและสวดมนต์อย่างลับๆ ให้ชาวบ้าน<br>
                  • พระเมเลตี ถูกตัดสินประหารชีวิตและถูกยิงเป้าเมื่อ 15.09.1937 (ได้รับการล้างมลทินแล้ว)
                </div>
              </div>
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I307'); switchTab('tree');" style="font-size:0.74rem;">🎯 พระภิกษุวิตาลี (เตอร์คิน)</button>
          </div>
        </div>

        <!-- 5. ЫБ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #05966933; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ หมู่บ้านอึบ — วัดพระเสด็จขึ้นสู่สวรรค์ (Holy Ascension)</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">ศาสนสถานบรรพชน (1827–1835)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เนินเขา 7 ลูกริมแม่น้ำซิโซลา • ชุมชนตระกูล: ซิโนเวียฟ, โปเลชชิคอฟ, ปาซินคอฟ</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดหินสีขาวตระหง่านบนยอดเขา สร้างเสร็จในปี ค.ศ. 1825–1835 เป็นศูนย์รวมพิธีกรรมทางศาสนาของบรรพบุรุษสายตระกูลซิโนเวียฟและโปเลชชิคอฟมาหลายชั่วอายุคน ทั้งการรับศีลจุ่มและการสมรสในทะเบียนประวัติ ค.ศ. 1834
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I50'); switchTab('tree');" style="font-size:0.74rem;">🎯 สายซิโนเวียฟ</button>
          </div>
        </div>

        <!-- 6. ЛОЙМА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ หมู่บ้านลอยมา — วัดแม่พระบรรทม (Dormition)</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">ชุมชนตระกูลซูตคินและเชโคนิน</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ลุ่มแม่น้ำลูซาตอนบน • เขตปรีลุซสกี</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดประวัติศาสตร์แห่งแขวงลอยมา ศูนย์กลางศรัทธาของตระกูลซูตคินและเชโคนิน ซึ่งปรากฏในทะเบียนสำมะโนศาสนจักรตั้งแต่ ค.ศ. 1748 เป็นต้นมา
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I21'); switchTab('tree');" style="font-size:0.74rem;">🎯 สายเชโคนิน</button>
          </div>
        </div>

        <!-- 7. УСТЬ-ВЫМЬ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #05966933; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ เมืองอุสต์-วิม — อารามหลวงอัครเทวทูตมีคาเอลและหมู่วัดโบราณ</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">ศูนย์กลางศาสนาแห่งโคมิ (1380+)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">จุดบรรจบแม่น้ำวิมและวิเชกดะ • เมืองหลวงโบราณแห่งเพิร์มดั้งเดิม</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ ศูนย์กลางการเผยแผ่ศาสนาคริสต์ในดินแดนเหนือ ก่อตั้งโดยนักบุญสเตฟานแห่งเปียร์ม ในปี ค.ศ. 1380 บรรพบุรุษตระกูลเตอร์คินได้รับแต่งตั้งเป็นเจ้าหน้าที่ผู้แทนฝ่ายคดีและที่ดินของพระสังฆราช (Prikaznoy chelovek) ประจำสำนักสงฆ์อุสต์-วิมมาตั้งแต่ศตวรรษที่ 17
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I274'); switchTab('tree');" style="font-size:0.74rem;">🎯 ต้นตระกูล ค.ศ. 1608</button>
          </div>
        </div>

        <!-- 8. ЛЯЛИ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #db277733; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#db2777;">⛪ หมู่บ้านลยาลี — วัดสมโภชพระคริสต์แสดงองค์ (Epiphany)</h3>
              <span style="background:#fdf2f8; color:#db2777; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fbcfe8;">ชุมชนตระกูลคารัคชีเยฟ</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ลุ่มแม่น้ำวิมตอนบน • ปรากฏในบันทึก ค.ศ. 1586</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดประจำตำบลโบราณแห่งลุ่มแม่น้ำวิม ชุมชนหลักของตระกูลคารัคชีเยฟและสายตระกูลชุกโตมอฟ บรรพชนได้มีส่วนร่วมในการสร้างและทำนุบำรุงวัดไม้และวัดหินของตำบล
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I23'); switchTab('tree');" style="font-size:0.74rem;">🎯 สายชุกโตมอฟ</button>
          </div>
        </div>

        <!-- 9. ОКВАД -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #0284c733; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#0284c7;">⛪ ตำบลอ็อควัด (คัตวัด) — วัดแม่พระเสด็จเข้าพระวิหาร</h3>
              <span style="background:#f0f9ff; color:#0284c7; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bae6fd;">อู่กำเนิดตระกูล (ศตวรรษที่ 17)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ริมแม่น้ำวิเชกดะ • แขวงอ็อควัดสกายา</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ ศาสนสถานประจำชุมชนอ็อควัด แหล่งกำเนิดสาแหรกตระกูลเตอร์คินและคิซยูรอฟก่อนการอพยพตั้งถิ่นฐาน ณ โคควิทซี บรรพชนร่วมถวายที่ดินและเครื่องบูชาแด่วัดตามบันทึกการตรวจราชการ ค.ศ. 1646
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I274'); switchTab('tree');" style="font-size:0.74rem;">🎯 ต้นตระกูล</button>
          </div>
        </div>

        <!-- 10. ПАЛЕВИЦЫ, СЕРЁГОВО, ЯРЕНСК -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ ปาเลวิทซี, เซเรโกโว, ยาเรนสค์</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">ชุมชนศาสนจักรลุ่มน้ำวิเชกดะ</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ศูนย์การปกครองและการค้าเกลือโบราณ</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ หมู่วัดวาอารามแห่งลุ่มน้ำวิเชกดะ ที่ซึ่งบรรพชนประกอบธุรกิจการค้า ขนส่งเกลือ และรับราชการแผ่นดินในฐานะผู้แทนชุมชนและผู้ตรวจราชการศาลศาสนจักร
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I19'); switchTab('tree');" style="font-size:0.74rem;">🎯 สายเตอร์คิน</button>
          </div>
        </div>

      </div>
    </div>"""
