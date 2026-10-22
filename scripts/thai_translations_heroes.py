#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/thai_translations_heroes.py
Full Thai translation for the WWII and WWI Heroes section (info-heroes).
"""

def get_thai_heroes_html():
    return """    <!-- WWII HEROES SECTION (THAI) -->
    <div class="info-card" id="info-heroes">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:1.6rem;">🎖️</span>
        <h2 style="margin:0;">วีรชนผู้พิทักษ์มาตุภูมิ: วีรบุรุษแห่งสงครามโลกครั้งที่สองและสงครามโลกครั้งที่หนึ่ง</h2>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.25rem; line-height:1.6;">
        ชีวประวัติและวีรกรรมการสู้รบของบรรพบุรุษที่มีเอกสารรับรองทางประวัติศาสตร์อย่างเป็นทางการ จากหอจดหมายเหตุกลางกระทรวงกลาโหมแห่งสหพันธรัฐรัสเซีย (TsAMO RF), หอจดหมายเหตุประวัติศาสตร์การทหารแห่งรัฐ (RGVIA), บันทึกสมุดบันทึกการรบของหน่วย (JBD) และคำสั่งปูนบำเหน็จเหรียญตราเกียรติยศ:
      </p>

      <div class="veteran-cards-grid">
        <!-- 1. ТУРКИН МИХАИЛ НИКОЛАЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#2563eb;">มิคาอิล นิโคลาเยวิช เตอร์คิน (Mikhail Nikolaevich Turkin)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">03.11.1906 – 02.09.1993 • หมู่บ้านโคควิทซี, โคมิ ASSR</div>
              </div>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #bfdbfe; white-space:nowrap;">รุ่นที่ 5 • คุณทวด</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">จ่าสิบเอกกองเกียรติยศ (Guards Senior Sergeant)</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">ผู้บังคับหมวดปืน ค. 82 มม.</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.6; margin-bottom:0.85rem;">
              <div><strong>หน่วยรบในสังกัด:</strong> กองพลน้อยยานยนต์รักษาพระองค์ที่ 18 ดเนียสตร์-คิงกัน ประดับเหรียญธงแดงและเครื่องราชอิสริยาภรณ์คูตูซอฟ ชั้นที่ 2 (กองพลน้อยยานยนต์รักษาพระองค์ที่ 9, กองทัพรถถังรักษาพระองค์ที่ 6); กองพลน้อยยานยนต์ที่ 45 (กองพลน้อยยานยนต์ที่ 5)</div>
              <div><strong>สมรภูมิและเส้นทางการรบ:</strong> แนวรบเบรียนสค์ (1942), แนวรบตะวันตกเฉียงใต้ (การป้องกันสมรภูมิสตาลินกราด), แนวรบตะวันตก, แนวรบยูเครนที่ 1 และ 2 (การรุกคืบในโรมาเนีย, ฮังการี, ยุทธการยึดกรุงเวียนนา ออสเตรีย, ปราก). <strong>ยุทธการทางยุทธศาสตร์แมนจูเรีย (สิงหาคม-กันยายน พ.ศ. 2488):</strong> แนวรบซาไบคัล การเดินทัพกรำศึก 800 กิโลเมตรฝ่าทะเลทรายโกบีและเทือกเขาเกรตเตอร์คิงกัน, การปลดปล่อยเมืองมุกเดน (เสิ่นหยาง), และการจับกุมกองทัพกวันตงของจักรวรรดิญี่ปุ่น</div>
              <div><strong>การเกณฑ์ทหาร:</strong> กองสัสดีเขตอุสต์-วิม, โคมิ ASSR. สมาชิกพรรคคอมมิวนิสต์ตั้งแต่ปี ค.ศ. 1943</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏅 เหรียญตราและเครื่องราชอิสริยาภรณ์แห่งรัฐบาล:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.6;">
                <li><strong>เครื่องราชอิสริยาภรณ์เกียรติยศ Order of Glory ชั้นที่ 3</strong> (คำสั่งกองพลน้อยยานยนต์รักษาพระองค์ที่ 18 ที่ 41/н ลงวันที่ 06.06.1945) — <em>สำหรับความกล้าหาญในการรบที่ออสเตรียและการรบประจัญบานตามถนนในกรุงเวียนนา: หมวดปืน ค. ทำลายปืนกลข้าศึก 3 จุด, กำจัดทหารฮิตเลอร์ 20 นาย, ระเบิดเกวียนบรรทุกกระสุนข้าศึก 3 คัน.</em> หนังสือเสนอชื่อลงนามโดยผู้บังคับการกองพลน้อย วีรบุรุษแห่งสหภาพโซเวียต พ.ท. ออฟชาโรฟ</li>
                <li><strong>เหรียญ "สำหรับความดีความชอบในการรบ" (Medal for Battle Merit)</strong> (คำสั่งกองพลน้อยยานยนต์ที่ 45 ที่ 37/н ลงวันที่ 03.08.1944) — <em>สำหรับการรบใกล้หมู่บ้านสตินกา (ประเทศโรมาเนีย) วันที่ 3–4 มิถุนายน 1944: หมวดปืน ค. ทำลายกำลังพลข้าศึก 20 นาย ขับไล่ทหารราบ 2 หมวด</em></li>
                <li><strong>การทำลายกองทัพกวันตง (แมนจูเรีย, 1945):</strong> เหรียญ "เพื่อชัยชนะเหนือญี่ปุ่น", หนังสือประกาศเกียรติคุณจากจอมพล โจเซฟ สตาลิน (คำสั่งที่ 372 ลงวันที่ 23.08.1945), กองพลน้อยได้รับนามเกียรติยศ "คิงกันสกายา"</li>
                <li><strong>เหรียญ "สำหรับการยึดกรุงเวียนนา" (Capture of Vienna)</strong> (09.06.1945)</li>
                <li><strong>เหรียญ "สำหรับการป้องกันสตาลินกราด" (Defence of Stalingrad)</strong> (22.12.1942)</li>
                <li><strong>เครื่องราชอิสริยาภรณ์สงครามปิตุภูมิ ชั้นที่ 1</strong> (06.04.1985)</li>
                <li><strong>เหรียญ "เพื่อชัยชนะเหนือเยอรมนีในสงครามรักชาติยิ่งใหญ่"</strong> (09.05.1945)</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>หอจดหมายเหตุ TsAMO RF: กองทุน 33, ทะเบียน 686196/690155; กองทุน 45 мехбр, ทะเบียน 1; สมุดบันทึกการรบ (JBD) ประจำวันที่ 3 มิถุนายน 1944.</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 เอกสารต้นฉบับและบันทึกประวัติศาสตร์ในหอจดหมายเหตุ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('turkin_slava_3')" style="font-size:0.74rem;">🔍 สแกน: Order of Glory</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_medal_zaslugi')" style="font-size:0.74rem;">🔍 สแกน: Battle Merit</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_jbd_3june1944_p26')" style="font-size:0.74rem;">⚔️ บันทึกการรบ 45 mbr: 3 มิ.ย. 1944</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_jbd_3june1944_crop')" style="font-size:0.74rem;">🎯 วีรกรรมหมวดปืน ค.</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_kniga_pamyati')" style="font-size:0.74rem;">📖 หนังสือบันทึกความทรงจำโคมิ</button>
                <button class="pill-btn" onclick="filterArchiveCategory('turkin'); switchTab('archive');" style="font-size:0.74rem;">📁 เอกสาร TsAMO ทั้งหมด 13 ฉบับ</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I19'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>

        <!-- 2. ТУРКИН ИВАН НИКОЛАЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#2563eb;">อีวาน นิโคลาเยวิช เตอร์คิน (Ivan Nikolaevich Turkin)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">เกิด 1918 • หมู่บ้านซูลาทุย (โคควิทซี), โคมิ ASSR</div>
              </div>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #bfdbfe; white-space:nowrap;">รุ่นที่ 5 • น้องชายคุณทวดมิคาอิล</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">ทหารกองทัพแดง (Red Army Soldier)</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">ผู้เข้าร่วมสงครามรักชาติยิ่งใหญ่</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.6; margin-bottom:0.85rem;">
              <div><strong>สายสัมพันธ์:</strong> บุตรคนเล็กของ นิโคไล อะเลคเซเยวิช เตอร์คิน และ พาฟลา อิวานอฟนา ซิเซวา, น้องชายร่วมบิดามารดาของ มิคาอิล นิโคลาเยวิช เตอร์คิน (คุณตาทวดร่วมสายเลือด)</div>
              <div><strong>ถิ่นกำเนิด:</strong> โคมิ ASSR, เขตอุสต์-วิม, สภาตำบลโคควิทซี, หมู่บ้านซูลาทุย (ซูลาตุยสกายา)</div>
              <div><strong>การระดมพล:</strong> ได้รับหมายเรียกเข้าประจำการเมื่อเดือนมิถุนายน ค.ศ. 1941 โดยกองสัสดีเมืองซิคตึฟคาร์</div>
              <div><strong>ความสำคัญต่อสาแหรกตระกูล:</strong> เป็นหลักฐานลายลักษณ์อักษรยืนยันความผูกพันอันแน่นแฟ้นระหว่างหมู่บ้านซูลาทุยและโคควิทซีของตระกูลเตอร์คิน</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#2563eb; margin-bottom:0.4rem;">📖 หลักฐานในหอจดหมายเหตุ:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.6;">
                <li>หนังสือบันทึกความทรงจำแห่งสาธารณรัฐโคมิ (Kniga Pamyati), เล่ม 6, หน้า 343</li>
                <li>ฐานข้อมูลทหารผ่านศึกแห่งสหพันธรัฐรัสเซีย</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>กองสัสดีเมืองซิคตึฟคาร์ โคมิ ASSR, มิถุนายน ค.ศ. 1941</em>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I68'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>

        <!-- 3. ЗИНОВЬЕВ ВЛАДИМИР СЕМЕНОВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #ec489933; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#db2777;">วลาดิมีร์ เซเมโนวิช ซิโนเวียฟ (Vladimir Semyonovich Zinoviev)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">เกิด ค.ศ. 1925 • หมู่บ้านโกเรลึย อึบ (โกเรซอยต์), โคมิ ASSR</div>
              </div>
              <span style="background:#fff1f2; color:#db2777; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fecdd3; white-space:nowrap;">รุ่นที่ 4 • พี่ชายของคุณย่าทวดอัลบินา</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">จ่าสิบตรี (Senior Sergeant)</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">ผู้บังคับหมู่ปืนครก กองร้อยปืนครกที่ 1</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>สายสัมพันธ์:</strong> บุตรของ เซเมียน กริกอเรียวิช ซิโนเวียฟ และ คลาฟดียา อิลยินิชนา คึซยูโรวา, พี่ชายแท้ๆ ของคุณย่าทวด อัลบินา เซเมนอฟนา กลาดึเชวา (ซิโนเวียวา), คุณตาทวดของคุณหนูนิโคไล</div>
              <div><strong>หน่วยรบในสังกัด:</strong> กรมทหารราบที่ 951, กองพลทหารราบไวบอร์กที่ 265 (กองพลน้อยทหารราบที่ 7, กองทัพจู่โจมที่ 3, แนวรบเบลารุสที่ 1; ก่อนหน้านี้ — แนวรบเลนินกราด และแนวรบบอลติกที่ 3)</div>
              <div><strong>เส้นทางแห่งการรบ:</strong> เข้าประจำการในกองทัพตั้งแต่วันที่ 2 มกราคม 1943 (เกณฑ์ทหารในวัยเพียง 17 ปี) ร่วมประจัญบานตั้งแต่วันที่ 19 กุมภาพันธ์ 1943 และได้รับบาดเจ็บในการรบเมื่อ 20 กุมภาพันธ์ 1943 ผ่านสมรภูมิคอคอดคาเรเลียปะทะกองทัพฟินแลนด์, ปลดปล่อยรัฐบอลติก, ยุทธการวิสตูลา-โอเดอร์, ปลดปล่อยกรุงวอร์ซอ และยุทธการบุกตีชิงกรุงเบอร์ลิน</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏅 เครื่องราชอิสริยาภรณ์และเหรียญตราเกียรติยศแห่งรัฐบาล:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>เครื่องราชอิสริยาภรณ์ดาวแดง (Order of the Red Star)</strong> (คำสั่งกองพลที่ 265 ที่ 18/н ลงวันที่ 06.03.1945) — <em>ในการรบตั้งรับทางเหนือของตำบลฮาเซินดอร์ฟ 18.02.1945 ในฐานะผู้บังคับหมู่ปืนครก ได้สั่งการยิงทำลายปืนกลและทหารข้าศึก 19 นาย</em></li>
                <li><strong>เครื่องราชอิสริยาภรณ์เกียรติยศ Order of Glory ชั้นที่ 3</strong> (คำสั่งกองพลที่ 265 ที่ 80/н ลงวันที่ 27.09.1944) — <em>ในการรบ ณ ตำบลวิลทอย 19.09.1944 หมู่ปืนครกได้ทำลายปืนกลหนัก 2 กระบอก และเครื่องยิงลูกระเบิด 1 กระบอก สกัดการตีโต้ตอบของข้าศึกได้ 2 ครั้ง</em></li>
                <li><strong>เหรียญ "เพื่อความกล้าหาญ" (Medal for Courage)</strong> (คำสั่งกรมที่ 951 ที่ 016-Н ลงวันที่ 15.07.1944) — <em>สำหรับความกล้าหาญในสมรภูมิคอคอดคาเรเลีย: ภายใต้พายุห่ากระสุนปืนใหญ่อันดุเดือด ได้ทำหน้าที่เล็งและบรรจุกระสุนด้วยตนเองจนปฏิบัติการสำเร็จ</em></li>
                <li><strong>เหรียญ "สำหรับการยึดกรุงเบอร์ลิน" (Medal for the Capture of Berlin)</strong> (ประกาศคำสั่ง 09.06.1945)</li>
                <li><strong>เหรียญ "สำหรับการปลดปล่อยกรุงวอร์ซอ" (Medal for the Liberation of Warsaw)</strong> (ประกาศคำสั่ง 09.06.1945)</li>
                <li><strong>เหรียญ "เพื่อชัยชนะเหนือเยอรมนีในสงครามรักชาติยิ่งใหญ่" (Medal for Victory over Germany)</strong> (09.05.1945)</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>TsAMO: กองทุน 33, บัญชี 686196, แฟ้ม 1311; บัญชี 687572, แฟ้ม 2112; บัญชี 690155, แฟ้ม 1302; ตู้ 35, กล่อง 8</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 เอกสารต้นฉบับและบันทึกประวัติศาสตร์ TsAMO:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <a href="pdf_документы/Зиновьев Владимир Семенович 1925.pdf" target="_blank" class="pill-btn" style="font-size:0.74rem;">📥 อัลบั้มเต็ม TsAMO (19 หน้า PDF)</a>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_red_star')" style="font-size:0.74rem;">🔍 สแกน: ดาวแดง (Red Star)</button>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_slava_3')" style="font-size:0.74rem;">🔍 สแกน: ตราเกียรติยศ (Order of Glory)</button>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_otvaga_list')" style="font-size:0.74rem;">🔍 สแกน: เพื่อความกล้าหาญ (For Courage)</button>
                <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_v'); switchTab('archive');" style="font-size:0.74rem;">📁 สแกน TsAMO ทั้ง 9 ฉบับ</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I67'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>

        <!-- 4. ЗИНОВЬЕВ СЕМЁН ГРИГОРЬЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #ec489933; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#db2777;">เซเมียน กริกอเรียวิช ซิโนเวียฟ (Semyon Grigoryevich Zinoviev)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">27.01.1890 – ? • หมู่บ้านโกเรลึย อึบ (อิบสกายา), โคมิ ASSR</div>
              </div>
              <span style="background:#fff1f2; color:#db2777; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fecdd3; white-space:nowrap;">รุ่นที่ 5 • คุณทวดเทียด</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">นายสิบแห่งกองทัพจักรวรรดิรัสเซีย (RIA Non-commissioned Officer)</span>
              <span class="badge-veteran">พลปืนใหญ่ชั้นผู้ใหญ่แห่งกองทัพแดง (Senior Gunner)</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">ทหารผ่านศึกสองสงครามโลก (WWI และ WWII)</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>สายสัมพันธ์:</strong> สามีของ คลาฟดียา อิลยินิชนา คึซยูโรวา, บิดาของ วลาดิมีร์ เซเมโนวิช ซิโนเวียฟ (วีรชนผู้บุกเบอร์ลิน) และคุณย่าทวด อัลบินา เซเมนอฟนา กลาดึเชวา (ซิโนเวียวา). คุณทวดเทียดของคุณหนูนิโคไล</div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>⚔️ สงครามโลกครั้งที่หนึ่ง (1914–1918):</strong>
                นายสิบ (เดิมพลทหารชั้นเอก) สังกัดกรมทหารราบโอสโตรเลนสกีที่ 181 (181st Ostrolensky Infantry Regiment, กองพลทหารราบที่ 46, กองพลทหารที่ 21). ร่วมยุทธการกาลีเซียและยุทธการกรากุฟ. ในสมรภูมิใกล้เมืองกรากุฟ (คอวาลี, กอสเตเลตส์, ซีโบโรวิทเซ) ระหว่างวันที่ 8–13 พฤศจิกายน 1914 สูญหายในการรบ; ถูกจับเป็นเชลยศึกเมื่อ 21.12.1914. ตั้งแต่วันที่ 15.01.1915 ถูกคุมขังในค่ายเชลยศึกมิโลวิทซ์ (Milowitz, จักรวรรดิออสเตรีย-ฮังการี ปัจจุบันอยู่ในเช็กเกีย). ภายหลังสงครามได้เดินทางกลับสู่แผ่นดินแม่โคมิ
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🛡️ สงครามรักชาติยิ่งใหญ่ (1941–1945):</strong>
                พลปืนใหญ่ชั้นผู้ใหญ่ กองร้อยที่ 7 กองพันทหารราบที่ 2 กรมทหารราบกองหนุนที่ 34 (34 зсп). ได้รับการเกณฑ์ระดมพลเข้าสู่กองทัพประจำการในวัยถึง 53 ปี (ค.ศ. 1943)
              </div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏛️ เอกสารจดหมายเหตุและพิพิธภัณฑ์ประวัติศาสตร์:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>สมุดประจำตัวทหารกองทัพแดง ลงวันที่ 13.06.1943</strong> («ผ่านเกณฑ์ตรวจสภาพร่างกาย 7.8.44») — พิพิธภัณฑ์กลางไอย์คิโน เขตอุสต์-วิม สาธารณรัฐโคมิ หมายเลข КП 8347 (เลขทะเบียน 21112145)</li>
                <li><strong>บัญชีรายชื่อผู้สูญเสียกรมทหารราบโอสโตรเลนสกีที่ 181 หมายเลข 31904</strong> — หอจดหมายเหตุประวัติศาสตร์การทหารแห่งรัฐ (RGVIA) กองทุน 16196, บัญชี 1, แฟ้ม 346</li>
                <li><strong>บัตรเชลยศึกค่ายมิโลวิทซ์ (Milowitz)</strong> — RGVIA บัญชีความสูญเสีย (เชลยศึก), ตู้ไม่มีหมายเลข, กล่อง 6292-K</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>RGVIA: กองทุน 16196, บัญชี 1, แฟ้ม 346; กล่อง 6292-K. พิพิธภัณฑ์กลางไอย์คิโน สหพันธ์พิพิธภัณฑ์เขตอุสต์-วิม</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 เอกสารต้นฉบับและบันทึกในหอจดหมายเหตุ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_s_krasnoarm_knizhka')" style="font-size:0.74rem;">🔍 สแกน: สมุดประจำตัวทหารแดง ค.ศ. 1943</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_plen_card_front')" style="font-size:0.74rem;">🛡️ สแกน: บัตรเชลยศึก (ค.ศ. 1915)</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_plen_card_back')" style="font-size:0.74rem;">📄 ด้านหลังบัตรเชลยศึก</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_spisok_poter_1914')" style="font-size:0.74rem;">⚔️ สแกน: บัญชีผู้สูญเสียกรมที่ 181 (ค.ศ. 1914)</button>
                <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_s'); switchTab('archive');" style="font-size:0.74rem;">📁 ทั้ง 4 เอกสารในคลัง</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I25'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>

        <!-- 5. ШУКТОМОВ АЛЕКСАНДР МИХАЙЛОВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#b45309;">อเล็กซานเดอร์ มิคาอิโลวิช ชุกโตมอฟ (Aleksandr Mikhailovich Shuktomov)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">1911 – กันยายน 1970 • หมู่บ้านเอรอซดีโน, โคมิ ASSR</div>
              </div>
              <span style="background:#fef3c7; color:#b45309; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fde68a; white-space:nowrap;">รุ่นที่ 5 • คุณทวดเทียด</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">พลทหารกองทัพแดง (Red Army Private)</span>
              <span class="badge-veteran">กรมทหารราบกองหนุนที่ 34 (34 зсп 29 зсд)</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">ผู้ร่วมรบในสงครามรักชาติยิ่งใหญ่</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>สายสัมพันธ์:</strong> สามีของ อัคนียา อิวานอฟนา ชุกโตโมวา (ปาซินโควา), บิดาของ ริมมา อะเลคซันดรอฟนา เตอร์คินา (ชุกโตโมวา). คุณทวดเทียดของคุณหนูนิโคไล</div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🛡️ สงครามรักชาติยิ่งใหญ่ (1941–1945):</strong>
                ระดมพลโดยกองสัสดีเขตอุสต์-วิม โคมิ ASSR ในเดือนธันวาคม 1941 เข้ารับการฝึกเป็นพลปืนเล็กในกองร้อยที่ 5 กองพันที่ 2 กรมทหารราบกองหนุนที่ 34 (34 зсп 29 зсд). วันที่ 18 มกราคม 1942 ส่งตัวพร้อมหมวดเดินทัพหมายเลข 43 สู่แนวหน้าในกองทัพประจำการ ปลดประจำการในเดือนกรกฎาคม 1942 ถึงแก่กรรมในเดือนกันยายน 1970 ในวัย 59 ปี
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🤝 จุดร่วมประวัติศาสตร์:</strong>
                รับราชการในกรมทหารราบกองหนุนที่ 34 (34 зсп 29 зсд) แห่งเดียวกันกับบรรพบุรุษอีกท่านหนึ่งของครอบครัว คือ พลปืนใหญ่ เซเมียน กริกอเรียวิช ซิโนเวียฟ
              </div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b45309; margin-bottom:0.4rem;">🏛️ บันทึกเอกสารหอจดหมายเหตุและต้นฉบับประวัติศาสตร์:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>บัญชีรายชื่อสถานีส่งกำลังทหาร กรมทหารราบกองหนุนที่ 34 กองพลที่ 29 ลงวันที่ 18.01.1942</strong> — TsAMO กองทุน 8312, บัญชี 37579с, แฟ้ม 3, เฟรม 38, รายการที่ 3526</li>
                <li><strong>หนังสืออนุสรณ์แห่งสาธารณรัฐโคมิ (Kniga Pamyati) ฉบับพิมพ์</strong> — เล่มที่ 6 หน้า 705 (บันทึกข้อมูลการระดมพล, การปลดประจำการ ก.ค. 1942 และวันถึงแก่กรรม ก.ย. 1970)</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>TsAMO: กองทุน 8312 (กรมทหารราบกองหนุนที่ 34 กองพลที่ 29), บัญชี 37579с, แฟ้ม 3; หนังสืออนุสรณ์แห่งสาธารณรัฐโคมิ (เล่ม 6)</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 เอกสารต้นฉบับและบันทึกในหอจดหมายเหตุ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('shuktomov_vpp_1942')" style="font-size:0.74rem;">🔍 สแกน: บัญชีกรมทหารราบที่ 34 (18.01.1942)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shuktomov_kniga_pamyati_komi')" style="font-size:0.74rem;">📖 สแกน: หนังสืออนุสรณ์แห่งสาธารณรัฐโคมิ (เล่ม 6)</button>
                <button class="pill-btn" onclick="filterArchiveCategory('shuktomov'); switchTab('archive');" style="font-size:0.74rem;">📁 ทั้ง 2 เอกสารในคลัง</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I23'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>

        <!-- 6. ШЕХОНИН МИХАИЛ АФАНАСЬЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #8b5cf633; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#7c3aed;">มิคาอิล อฟานาซีเยวิช เชโคนิน (Mikhail Afanasyevich Shekhonin)</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">1909 – พฤศจิกายน 1988 • หมู่บ้านลอยมา, โคมิ ASSR</div>
              </div>
              <span style="background:#f5f3ff; color:#7c3aed; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #ddd6fe; white-space:nowrap;">รุ่นที่ 5 • คุณทวด</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">ร้อยตรีแห่งกองทัพแดง (Junior Lieutenant RKKA)</span>
              <span class="badge-veteran">กรมทหารราบที่ 995 กองพลทหารราบที่ 263</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.6; margin-bottom:0.85rem;">
              <div><strong>หน่วยรบและสมรภูมิ:</strong> กรมทหารราบที่ 995, กองพลทหารราบที่ 263 (แนวรบคาเรเลียและแนวรบตอนเหนือ). ได้รับบาดเจ็บสาหัสจากการรบประจัญบานในการปกป้องดินแดนทางตอนเหนือของรัสเซีย</div>
              <div><strong>การรักษาพยาบาลและการปลดประจำการ:</strong> รับการรักษาในกองพันเสนารักษ์ที่ 25 (25 medsanbat) และโรงพยาบาลสนามทหาร ЭГ 1438 / ЭГ 2513 ปลดประจำการเนื่องจากบาดแผลสงครามในเดือนมกราคม ค.ศ. 1943</div>
              <div><strong>สายสัมพันธ์:</strong> บิดาของ เอมิเลีย มิคาอิโลฟนา เชโคนินา (คุณยาย), ต้นตระกูลเชโคนินแห่งลอยมา</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#7c3aed; margin-bottom:0.4rem;">🏅 เหรียญตราเกียรติยศแห่งรัฐบาล:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.6;">
                <li><strong>เครื่องราชอิสริยาภรณ์สงครามปิตุภูมิ ชั้นที่ 1 (Order of the Patriotic War I class)</strong> (คำสั่งกระทรวงกลาโหมสหภาพโซเวียต ที่ 89 ลงวันที่ 06.04.1985) — สำหรับความกล้าหาญและบาดแผลจากการรบเพื่อมาตุภูมิ</li>
                <li><strong>เหรียญ "เพื่อชัยชนะเหนือเยอรมนี"</strong></li>
              </ul>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 เอกสารต้นฉบับในหอจดหมายเหตุ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_kniga_pamyati_komi_full')" style="font-size:0.74rem;">📖 สแกน: Kniga Pamyati (เล่ม 5, หน้า 612)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_card_ranenie_vmd')" style="font-size:0.74rem;">🏥 ทะเบียนการรักษาบาดแผล (TsAMO VMD)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_yubileinaya_kartoteka_1985')" style="font-size:0.74rem;">🎖️ เครื่องราชฯ สงครามปิตุภูมิ ชั้น 1</button>
                <button class="pill-btn" onclick="filterArchiveCategory('shekhonin'); switchTab('archive');" style="font-size:0.74rem;">📁 เอกสารเชโคนินทั้ง 4 ฉบับ</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I21'); switchTab('tree');" style="font-size:0.78rem;">🎯 ดูตำแหน่งในสาแหรก</button>
          </div>
        </div>
      </div>
    </div>"""
