#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/thai_translations_clergy.py
Full-length, comprehensive Thai translation for the Orthodox Clergy
and Parish Churches section (info-clergy). All 10 cards fully articulated.
"""

def get_thai_clergy_html():
    return """    <!-- ORTHODOX CLERGY & PARISH CHURCHES SECTION (THAI - FULL DETAILED) -->
    <div class="info-card" id="info-clergy">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:1.6rem;">⛪</span>
        <h2 style="margin:0;">คณะสงฆ์ออร์โธดอกซ์และศาสนสถานของบรรพบุรุษ (คริสต์ศตวรรษที่ 17–20, ค.ศ. 1646–1937)</h2>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.2rem; line-height:1.6;">
        ตลอดเวลากว่าสามศตวรรษ — ตั้งแต่สมุดทะเบียนราษฎร์ศตวรรษที่ 17 จนถึงศตวรรษที่ 20 — จิตวิญญาณและวิถีชีวิตประจำวันของบรรพชนทุกชั่วคนผูกพันแนบแน่นกับอารามหลวงและวัดประจำตำบลในแขวงยาเรนสค์, อุสต์-วิม และอุสต์-ซีโซลสค์ แห่งมณฑลโวล็อกดา (ปัจจุบันคือสาธารณรัฐโคมิและแคว้นคิรอฟ). ตระกูลเตอร์คินได้ให้กำเนิดวงศ์วานสงฆ์ชั้นสูง สังฆานุกรประจำมหาวิหาร ไวยาวัจกร และพระภิกษุอารามหลวง ขณะที่ทุกสายตระกูลร่วมสาแหรก (ชุกโตมอฟ, ซิโนเวียฟ, ซูตคิน, โปเลชชิคอฟ, ปาซินคอฟ, คิซยูรอฟ, เลทอฟ, ยารานอฟ) ล้วนประกอบพิธีศีลจุ่ม ศีลสมรส และพิธีปลงศพ ณ ศาสนสถานศักดิ์สิทธิ์เหล่านี้
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
              <h3 style="margin:0; font-size:1.05rem; color:#2563eb;">🏛️ หมู่บ้านโคควิทซี — วัดพระคริสตสมภพ (Christ the Nativity)</h3>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bfdbfe;">ศูนย์กลางจิตวิญญาณตระกูล (150+ ปี)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เนินเขาโคควิทสกายา โกรา, แขวงยาเรนสค์ • ชุมชนหลักของตระกูล: เตอร์คิน, เลทอฟ, ยารานอฟ, ซิเซฟ</div>
            
            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png', 'วัดพระคริสตสมภพ ณ หมู่บ้านโคควิทซี', 'สมุดบันทึกการสารภาพบาป ค.ศ. 1773 ครัวเรือนที่ 167 ของบาทหลวงสเตปาน เตอร์คิน')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png" alt="ทะเบียนวัดโคควิทซี 1773" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>📜 วัดหินสองชั้นอันสง่างาม สร้างขึ้นในปี ค.ศ. 1820–1837 (แทนที่วัดไม้เดิมแห่งศตวรรษที่ 17–18) เป็นศูนย์รวมใจของชาวเนินเขาโคควิทซี 20 หมู่บ้าน</div>
                <div style="margin-top:0.35rem;">👶 ในสมุดทะเบียนเกิดของวัด มีการบันทึกการถือกำเนิดของคุณทวด <strong>นิโคไล อะเลคเซเยวิช เตอร์คิน</strong> เมื่อวันที่ 3 พฤศจิกายน ค.ศ. 1876 (หมู่บ้านซูลาทุย, บันทึก ณ หน้า 267)</div>
              </div>
            </div>

            <p style="font-size:0.83rem; line-height:1.55; margin-bottom:0.65rem;">
              อู่กำเนิดวงศ์วานสงฆ์และการรับใช้อย่างต่อเนื่องยาวนานหลายชั่วรุ่นของตระกูลเตอร์คิน:
            </p>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>บาทหลวง (Ierey):</strong> บาทหลวงสเตฟาน อิวาโนวิช เตอร์คิน (รับใช้ ค.ศ. 1734–1773, สำมะโนนักบวชปี 1773 บ้านเลขที่ 167 ในวัย 62 ปี ม่าย); บาทหลวงอีวาน เปโตรวิช เตอร์คิน (ผู้ช่วยพิธีกรรม ค.ศ. 1710, บวชเป็นบาทหลวง ค.ศ. 1747)</li>
              <li><strong>สังฆานุกร (Deacon):</strong> อะเลคซี เยลิเซเยวิช เตอร์คิน (ผู้ช่วยพิธีกรรม ค.ศ. 1818, บวชเป็นสังฆานุกร ค.ศ. 1822, รับใช้ถึง ค.ศ. 1844+)</li>
              <li><strong>พลสวดและผู้ช่วยพิธีกรรม:</strong> เลออนตี เปโตรวิช (1732–1783); เยลิเซย์ เลออนเตียวิช (บวชปี 1783 โดยมุขนายกโยอันน์, รับใช้ยาวนานกว่า 33 ปี, ภรรยา ทาเทียนา วาซิลเยฟนา โปโนมาเรวา); ปีเตอร์ เปโตรวิช (เกิดราว ค.ศ. 1714)</li>
              <li><strong>บุตรหลานในคณะสงฆ์:</strong> อีวาน (ผู้ช่วยสวด), มักซิม, กัฟริอิล, ดมิทรี (ตามทะเบียนสำมะโน ค.ศ. 1795 และ 1811)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I78'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงสเตฟาน</button>
            <button class="pill-btn" onclick="focusPerson('I234'); switchTab('tree');" style="font-size:0.74rem;">🎯 สังฆานุกรอะเลคซี</button>
            <button class="pill-btn" onclick="focusPerson('I232'); switchTab('tree');" style="font-size:0.74rem;">🎯 เยลิเซย์</button>
          </div>
        </div>

        <!-- 2. ЛАЛЬСК -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #7c3aed33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#7c3aed;">⛪ เมืองลัลสค์ — มหาวิหารพระคืนชนม์ (Resurrection Cathedral)</h3>
              <span style="background:#f5f3ff; color:#7c3aed; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #ddd6fe;">สังฆานุกรประจำมหาวิหาร (1870–1904)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เมืองลัลสค์ สังฆมณฑลโวล็อกดา (ปัจจุบันคือแคว้นคิรอฟ) • อัญมณีบาโรก ค.ศ. 1698–1715</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Лальск_Воскресенский_собор.jpg', 'มหาวิหารพระคืนชนม์ ณ เมืองลัลสค์', 'มหาวิหารหินสร้างเมื่อ ค.ศ. 1717 • สถานที่ปฏิบัติศาสนกิจของสังฆานุกร มิคาอิล อะเลคเซเยวิช เตอร์คิน (1870–1904)')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="фото_храмов/Лальск_Воскресенский_собор.jpg" alt="มหาวิหารลัลสค์" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🏛️ มหาวิหารหินห้ายอดอันสง่างาม พร้อมหอระฆังทรงกระโจมสูงตระหง่าน ศูนย์กลางการค้าและจิตวิญญาณแห่งลุ่มแม่น้ำลูซา</div>
                <div style="margin-top:0.35rem;">📜 ภาพถ่ายประวัติศาสตร์โดย ส. โลโบวิคอฟ ช่างภาพระดับตำนานแห่งจักรวรรดิรัสเซีย บันทึกภาพไว้ในช่วงที่สังฆานุกรมิคาอิล เตอร์คิน กำลังปฏิบัติศาสนกิจ</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>สังฆานุกรประจำมหาวิหาร มิคาอิล อะเลคเซเยวิช เตอร์คิน</strong> (ราว 1839 – 14.06.1904) — บุตรสังฆานุกรอะเลคซีแห่งโคควิทซี สำเร็จการศึกษาจากวิทยาลัยศาสนศาสตร์โวล็อกดา (ค.ศ. 1862). เริ่มรับใช้เป็นผู้ช่วยสวดตั้งแต่ปี 1868, บวชเป็นสังฆานุกรเมื่อวันที่ 20.07.1870, และตั้งแต่ปี 1871 ดำรงตำแหน่งสังฆานุกรประจำมหาวิหารพระคืนชนม์แห่งเมืองลัลสค์ (รับใช้อย่างซื่อสัตย์ยาวนานถึง 34 ปี, กองทุน GAKO หมายเลข 1310). สมรสกับ โซเฟีย โปรโคเปียฟนา บรึซกาโลวา</li>
              <li><strong>ต้นตระกูลสายสงฆ์แห่งลัลสค์:</strong> อบรมบุตรหลานในธรรมเนียมของชนชั้นนักบวช ให้กำเนิดวงศ์วานสงฆ์รุ่นใหม่แห่งมณฑลโวล็อกดา</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I236'); switchTab('tree');" style="font-size:0.74rem;">🎯 สังฆานุกรมิคาอิลแห่งลัลสค์</button>
          </div>
        </div>

        <!-- 3. КАДНИКОВ, ВОЛОГДА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #9333ea33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#9333ea;">⛪ เมืองคัดนิคอฟ, โวล็อกดา, กรียาโซเวตส์ — ชุมชนวัดของบาทหลวงโปรโคปี (Parishes of Fr. Prokopy)</h3>
              <span style="background:#faf5ff; color:#9333ea; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #e9d5ff;">บาทหลวงประจำตำบล (1891–1915+)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">สังฆมณฑลโวล็อกดา • แขวงคัดนิคอฟ, โวล็อกดา และเกรียโซเวทส์ • ค.ศ. 1891–1915+</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Брусничное_Спасо_Преображенская_церковь.jpg', 'หมู่บ้านสปัสสโกเย — วัดการแปรสภาพของพระเยซูเจ้า', 'วิหารหินสร้าง ค.ศ. 1869–1884 • ชุมชนวัดของบาทหลวงโปรโคปี เตอร์คิน')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
                <img src="фото_храмов/Брусничное_Спасо_Преображенская_церковь.jpg" alt="วัดบรูสนิชโนเย" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </div>
              <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
                <div>🏛️ วัดการแปรสภาพของพระเยซูเจ้าบนเขาตาบอร์ ณ บรูสนิชโนเย (Spaso-Preobrazhenskaya, สปัสสโคเย แขวงโวล็อกดา) สร้างด้วยหินอันสง่างาม ค.ศ. 1869–1884 ประจำการตั้งแต่วันที่ 13.09.1911</div>
                <div style="margin-top:0.35rem;">📜 ก่อนหน้านั้น บาทหลวงโปรโคปีรับใช้เป็นเจ้าอาวาสวัดนิโคลาเยฟสกายา ณ ปุสโตรัมยานสกายา (แขวงคัดนิคอฟ) นานถึง 14 ปี และบวชสังฆานุกร ณ วัดอุสเปนสกายา (แขวงเกรียโซเวทส์) ในปี 1891</div>
              </div>
            </div>

            <p style="font-size:0.83rem; line-height:1.55; margin-bottom:0.65rem;">
              เส้นทางการรับใช้ศาสนาของบุตรสังฆานุกรมิคาอิลแห่งลัลสค์ ในแขวงตอนกลางของมณฑลโวล็อกดา:
            </p>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>บาทหลวง โปรโคปี มิคาอิโลวิช เตอร์คิน</strong> (เกิดราว 1868 ณ เมืองลัลสค์) — สำเร็จการศึกษาจากวิทยาลัยศาสนศาสตร์โวล็อกดา ได้รับการตั้งชื่อตามคุณตา โปรโคปี บรึซกาลอฟ คหบดีใหญ่เมืองโซลวิเชกอดสค์</li>
              <li><strong>วัดอุสเปนสกายา แชร์เน็ตสกายา (แขวงเกรียโซเวทส์):</strong> บวชเป็นสังฆานุกรเมื่อ 30.08.1891 (จดหมายเหตุสังฆมณฑลโวล็อกดา VEB 1891, ฉบับ 20, หน้า 305)</li>
              <li><strong>วัดนิโคลาเยฟสกายา ปุสโตรัมยานสกายา (แขวงคัดนิคอฟ):</strong> บวชเป็นบาทหลวงในปี 1897 และดำรงตำแหน่งเจ้าอาวาสยาวนานถึง 14 ปี</li>
              <li><strong>วัดสปัสโซ-เปรออบราเซนสกายา ณ บรูสนิชโนเย (แขวงโวล็อกดา):</strong> เป็นเจ้าอาวาสตั้งแต่วันที่ 13.09.1911 (VEB 1911, ฉบับ 19, หน้า 376; ฐานข้อมูล parishes.ru เลขที่ 7463)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I260'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงโปรโคปี</button>
            <button class="pill-btn" onclick="focusPerson('I236'); switchTab('tree');" style="font-size:0.74rem;">🎯 บิดา สังฆานุกรมิคาอิล</button>
          </div>
        </div>

        <!-- 4. УЛЬЯНОВО И КУЖБА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #4f46e533; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#4f46e5;">⛪ หมู่บ้านอูลยานอโว และ คุจวา — อารามหลวงตรีเอกภาพ-นักบุญสเตฟาน (Trinity-Stefanovsky Monastery)</h3>
              <span style="background:#eef2ff; color:#4f46e5; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #c7d2fe;">ผู้สละชีพเพื่อศรัทธา ศตวรรษที่ 20</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">แขวงอุสต์-ซีโซลสค์และอุสต์-คุลอม • ลุ่มแม่น้ำวิเชกดะตอนบน • ค.ศ. 1865–1937</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <div onclick="openFullscreenScan('фото_храмов/Ульяново_Троице_Стефановский_монастырь.jpg', 'หมู่บ้านอูลยานอโว — อารามหลวงตรีเอกภาพ-นักบุญสเตฟาน', 'อารามหลวงเซนต์สเตฟานแห่งเปียร์ม • วีรกรรมแห่งศรัทธาของพระภิกษุวิตาลี (เตอร์คิน), ค.ศ. 1937')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex-shrink:0;">
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
              <div onclick="openFullscreenScan('архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg', 'พระมรณสักขี เมเลตี (เฟดิวเนียฟ)', 'พระเหรัญญิกอารามหลวง ผู้ร่วมคดีความปี 1937 เดียวกันกับพระภิกษุวิตาลี เตอร์คิน')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex:0 0 92px; text-align:center;">
                <img src="архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg" alt="พระมรณสักขี เมเลตี" style="width:92px; height:118px; object-fit:cover; border-radius:6px; border:1.5px solid #7c3aed; box-shadow:0 2px 5px rgba(0,0,0,0.15); display:block; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'" />
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
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ หมู่บ้านอึบ — วัดพระเยซูเสด็จขึ้นสู่สวรรค์ (Holy Ascension)</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">วัดประจำตำบลของบรรพชน (1827–1835)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">เนินเขา 7 ลูกริมแม่น้ำซิโซลา, แขวงอุสต์-ซีโซลสค์ • ชุมชนหลักของตระกูล: ซิโนเวียฟ, โปเลชชิคอฟ, ปาซินคอฟ</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดหินสีขาวตระหง่านบนยอดเขา สร้างเสร็จในปี ค.ศ. 1825–1835 ตามแบบสถาปัตยกรรมคลาสสิกอันสง่างามของมุขมณฑลโวล็อกดา เป็นศูนย์รวมจิตใจและสถานที่ประกอบศีลศักดิ์สิทธิ์ของบรรพชนหลายชั่วรุ่น:
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>สายตระกูลซิโนเวียฟ (Zinoviev) แห่งหมู่บ้านโกเรลึย อึบ:</strong> สเตปัน ซิโนเวียฟ (เกิด 1790), คอนดราตี สเตปาโนวิช (เกิด 1813), กริกอรี คอนดราเตียวิช (เกิด 1860) และคุณทวด เซเมียน กริกอเรียวิช ซิโนเวียฟ (เกิด 27.01.1890 ทหารผ่านศึกสงครามโลกครั้งที่หนึ่ง) ล้วนประกอบพิธีศีลจุ่มและศีลสมรสในวัดนี้ตามบันทึกทะเบียนศาสนจักร ค.ศ. 1834 และ 1912</li>
              <li><strong>สายตระกูลโปเลชชิคอฟ (Poleshchikov):</strong> แอนนา วาซิลเยฟนา โปเลชชิโควา (คุณทวด 6 ชั่วคน เกิด 1782)</li>
              <li><strong>สายตระกูลปาซินคอฟ (Pasynkov):</strong> มาเรีย ปาซินโควา (คุณทวด 7 ชั่วคน เกิด 1761)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I50'); switchTab('tree');" style="font-size:0.74rem;">🎯 เซเมียน ซิโนเวียฟ</button>
            <button class="pill-btn" onclick="focusPerson('I51'); switchTab('tree');" style="font-size:0.74rem;">🎯 กริกอรี ซิโนเวียฟ</button>
          </div>
        </div>

        <!-- 6. ЛОЙМА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ หมู่บ้านลอยมา — วัดแม่พระบรรทม (Dormition of the Theotokos)</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">วัดประจำตำบลของตระกูลซูตคินและเชโคนิน</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ลุ่มแม่น้ำลูซาตอนบน, แขวงเวลีโคอุสติยูกและปรีลุซสกี • ค.ศ. 1748–1917+</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดหินหลังใหญ่สร้างเสร็จในปี ค.ศ. 1812 แทนวัดไม้ดั้งเดิมที่ปรากฏในทะเบียนศาสนจักรมาตั้งแต่ปี ค.ศ. 1748 ศูนย์กลางศรัทธาของบรรพบุรุษสายใต้:
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>สายตระกูลซูตคิน (Syutkin):</strong> บรรพบุรุษสายตรง ยาคอฟ มักซีโมวิช ซูตคิน (เกิด 1756), อิวาน ยาคอฟเลวิช (เกิด 1789) และ เปลาเกีย อิวานอฟนา ซูตคินา (เกิด 1817, คุณทวด 5 ชั่วคน) ล้วนได้รับการจดบันทึกในทะเบียนศีลจุ่มและสำมะโนครัวของวัดลอยมาอย่างต่อเนื่อง</li>
              <li><strong>สายตระกูลเชโคนิน (Shekhonin):</strong> บรรพชนสายคุณยาย เอมิเลีย มิคาอิโลฟนา เชโคนินา และคุณทวด ร้อยตรี มิคาอิล อฟานาซีเยวิช เชโคนิน (เกิด ค.ศ. 1909 วีรชนสงครามโลกครั้งที่สอง)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I24'); switchTab('tree');" style="font-size:0.74rem;">🎯 เปลาเกีย ซูตคินา</button>
            <button class="pill-btn" onclick="focusPerson('I21'); switchTab('tree');" style="font-size:0.74rem;">🎯 มิคาอิล เชโคนิน</button>
          </div>
        </div>

        <!-- 7. УСТЬ-ВЫМЬ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #05966933; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ ชุมชนอุสต์-วิม — อารามหลวงอัครเทวทูตมีคาเอลและหมู่วัดประวัติศาสตร์ (Ust-Vym)</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">ศูนย์กลางศาสนาแห่งโคมิ (1380+)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">จุดบรรจบแม่น้ำวิมและวิเชกดะ • เมืองหลวงโบราณแห่งเพิร์มดั้งเดิม</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ ดินแดนศักดิ์สิทธิ์ศูนย์กลางการเผยแผ่ศาสนาคริสต์ในดินแดนเหนือ ก่อตั้งโดยนักบุญสเตฟานแห่งเปียร์ม ในปี ค.ศ. 1380 เป็นที่พำนักของสามมุขนายกศักดิ์สิทธิ์แห่งเพิร์ม (เกราซิม, ปิติริม และโยนาห์) บรรพบุรุษตระกูลเตอร์คินมีความผูกพันลึกซึ้ง:
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>ค.ศ. 1646:</strong> อฟานาซี เซเมโนวิช เตอร์คิน ดำรงตำแหน่งข้าราชการผู้แทนพระสังฆราช (Prikaznoy chelovek) ประจำสำนักสงฆ์และตำบลอุสต์-วิม ตามสำมะโนของอีวาน สเกรียบิน</li>
              <li><strong>ค.ศ. 1688–1698:</strong> อีซาค อฟานาซีเยวิช เตอร์คิน ได้รับเลือกตั้งเป็นผู้พิพากษาประจำตำบลอุสต์-วิม (Vyborny sudya) ทำหน้าที่ตัดสินคดีความ ณ ศาลแขวงอุสต์-วิม</li>
              <li><strong>ค.ศ. 1731:</strong> อะเลคซี อิวาโนวิช เตอร์คิน บรรพบุรุษสายตรง ได้รับการบันทึกในเอกสารศาสนจักรประจำแขวง</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี (1646)</button>
            <button class="pill-btn" onclick="focusPerson('I75'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีซาค (1688)</button>
          </div>
        </div>

        <!-- 8. ЛЯЛИ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #db277733; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#db2777;">⛪ หมู่บ้านลยาลี — วัดสมโภชพระคริสต์แสดงองค์ (Epiphany Church)</h3>
              <span style="background:#fdf2f8; color:#db2777; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fbcfe8;">ชุมชนตระกูลคารัคชีเยฟและชุกโตมอฟ</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ลุ่มแม่น้ำวิมตอนบน, แขวงยาเรนสค์ • ปรากฏในบันทึกพงศาวดาร ค.ศ. 1586</div>

            <div style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              🏛️ วัดประจำตำบลโบราณแห่งลุ่มแม่น้ำวิม วัดไม้เดิมสร้างขึ้นในศตวรรษที่ 16 และวัดหินสองชั้นหลังใหญ่สร้างเสร็จในปี ค.ศ. 1845 เป็นศูนย์รวมจิตใจของบรรพชน:
            </div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>สายตระกูลคารัคชีเยฟ (Karakchiev):</strong> ปรากฏในสมุดสำมะโน ค.ศ. 1678 และ 1710 ชุมชนบ้านเลขที่ 15 ประจำตำบลลยาลี บรรพบุรุษสายตรงของครอบครัว</li>
              <li><strong>สายตระกูลชุกโตมอฟ (Shuktomov):</strong> บรรพชนสายคุณยายทวด แอนนา อเล็กซานดรอฟนา ชุกโตโมวา และคุณทวด อเล็กซานเดอร์ มิคาอิโลวิช ชุกโตมอฟ (เกิด 1911) ทหารผ่านศึกสงครามโลกครั้งที่สอง</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I23'); switchTab('tree');" style="font-size:0.74rem;">🎯 อเล็กซานเดอร์ ชุกโตมอฟ</button>
            <button class="pill-btn" onclick="focusPerson('I25'); switchTab('tree');" style="font-size:0.74rem;">🎯 สายคารัคชีเยฟ</button>
          </div>
        </div>

        <!-- 9. ОКВАД -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #0284c733; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#0284c7;">⛪ ชุมชนโบราณอ็อควัด (คัตวัด) — วัดแม่พระเสด็จเข้าพระวิหาร (Vvedenskaya)</h3>
              <span style="background:#f0f9ff; color:#0284c7; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bae6fd;">อู่กำเนิดตระกูล (ศตวรรษที่ 17)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ตำบลอ็อควัดสกายา, แขวงยาเรนสค์ • คริสต์ศตวรรษที่ 17–18</div>

            <p style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin-bottom:0.65rem;">
              ถิ่นกำเนิดดั้งเดิมและเก่าแก่ที่สุดของตระกูลเตอร์คินที่มีหลักฐานเป็นลายลักษณ์อักษรริมแม่น้ำวิเชกดะ:
            </p>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>ปฐมบรรพบุรุษผู้สถาปนาวงศ์:</strong> อฟานาซี เซเมโนวิช เตอร์คิน (เกิดราว ค.ศ. 1600) — ข้าราชการผู้แทนฝ่ายอาณาจักรของพระสังฆราช (Prikaznoy chelovek) ตามสำมะโนปี ค.ศ. 1646 (RGADA ฟ. 1209, เล่ม 1080) ดูแลรายได้และที่ดินของพระอัครสังฆราชโวล็อกดาและเวลีโคเปียร์ม</li>
              <li><strong>ผู้ช่วยพิธีกรรมและไวยาวัจกร:</strong> อีซาค อฟานาซีเยวิช เตอร์คิน (เกิด ค.ศ. 1635, อายุ 11 ปีในปี 1646) — ผู้ช่วยพิธีกรรมประจำวัดเวเดนสกายา (สมุดสำมะโน ค.ศ. 1678) และผู้ช่วยสวด (ค.ศ. 1696/97)</li>
              <li><strong>บาทหลวง:</strong> บาทหลวง อัฟโตนอม ลาฟเรนเตียวิช เตอร์คิน (เกิดราว ค.ศ. 1690) — เจ้าอาวาสวัดเวเดนสกายา ในปี ค.ศ. 1731 และ 1736 (สมุดทะเบียน GAAF ฟ. 29, บันทึก VUTsA ฟ. 363)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 อฟานาซี</button>
            <button class="pill-btn" onclick="focusPerson('I73'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีซาค</button>
            <button class="pill-btn" onclick="focusPerson('I245'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงอัฟโตนอม</button>
          </div>
        </div>

        <!-- 10. ПАЛЕВИЦЫ И ДР. -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ ปาเลวิทซี, เซเรโกโว, ยาเรนสค์ — ศูนย์กลางศาสนจักรลุ่มน้ำวิเชกดา (Palevitsy, Seryogovo, Yarensk)</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">ชุมชนศาสนจักรลุ่มน้ำวิเชกดะ</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">ปาเลวิทซี, เซเรโกโว, เคเนียซโปโกสต์ และมหาวิหารแห่งเมืองยาเรนสค์</div>

            <ul style="font-size:0.82rem; line-height:1.6; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>หมู่บ้านปาเลวิทซี (วัดโปครอฟสกายา):</strong> บาทหลวง อะเลคซี ติโมเฟเยวิช เตอร์คิน (รับใช้ ค.ศ. 1734–1758, ภรรยา มาโตรนา, บุตร มิคาอิล, อันเดรย์, มาร์ฟา); ผู้ช่วยพิธีกรรม อีวาน เปโตรวิช เตอร์คิน (ค.ศ. 1747)</li>
              <li><strong>หมู่บ้านเซเรโกโว และ เคเนียซโปโกสต์:</strong> พลสวดและผู้ช่วยพิธีกรรม อีวาน เยลิเซเยวิช เตอร์คิน (ค.ศ. 1802–1815+)</li>
              <li><strong>เมืองยาเรนสค์ (มหาวิหารสปัสโซ-เปรออบราเซนสกี):</strong> ผู้ดูแลรักษามหาวิหาร มิคาอิล อะเลคเซเยวิช เตอร์คิน (ตั้งแต่ปี 1755, ภรรยา มาร์ฟา คอซมินิชนา อิปาโตวา)</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I239'); switchTab('tree');" style="font-size:0.74rem;">🎯 บาทหลวงอะเลคซี</button>
            <button class="pill-btn" onclick="focusPerson('I238'); switchTab('tree');" style="font-size:0.74rem;">🎯 อีวาน</button>
            <button class="pill-btn" onclick="focusPerson('I241'); switchTab('tree');" style="font-size:0.74rem;">🎯 มิคาอิล</button>
          </div>
        </div>

      </div>
    </div>"""
