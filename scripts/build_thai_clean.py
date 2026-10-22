#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_thai_clean.py
Generates thai.html from index.html with complete idiomatic Thai translation
for the entire "Places and Roots" (ถิ่นกำเนิดและสายตระกูล) section:
1. About Family (info-overview)
2. WWII & WWI Heroes (info-heroes)
3. Orthodox Clergy & Churches (info-clergy)
4. 17th Century Court Battles & Civil Service (info-court-cases)
5. Historical Geography of 14 Villages (info-geography)
6. Onomastics of 18 Surnames (info-surnames)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.thai_translations_all import THAI_TRANSLATIONS_ALL
from scripts.thai_translations_heroes import get_thai_heroes_html
from scripts.thai_translations_clergy import get_thai_clergy_html
from scripts.thai_translations_court import get_thai_court_html

def build_thai_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Overview Card
    thai_overview_card = """    <!-- OVERVIEW -->
    <div class="info-card" id="info-overview">
      <h2>🌳 เกี่ยวกับครอบครัวและโครงสร้างสาแหรกตระกูล</h2>
      <p>สาแหรกตระกูลนี้รวบรวมขึ้นจากเอกสารลายลักษณ์อักษรต้นฉบับโบราณ ทะเบียนประวัติครอบครัว ทะเบียนการเกิด-การสมรส-การเสียชีวิตของศาสนจักร (Metric Books) และสำมะโนประชากรทางการ (Revision Lists) ย้อนรอยตั้งแต่คริสต์ศตวรรษที่ 17 ถึง 20 โดยจุดเริ่มต้นของสาแหรกนี้ (Proband) คือ <strong>ด.ช. นิโคไล วยาเชสลาโววิช เตอร์คิน (Nikolai Turkin)</strong> เกิดเมื่อปี พ.ศ. 2567 ณ อำเภอเมือง จังหวัดชุมพร ประเทศไทย</p>
      <p>สาแหรกตระกูลนี้เป็นการหลอมรวมสองสายธารประวัติศาสตร์ วัฒนธรรม และภูมิศาสตร์อันยิ่งใหญ่ที่อยู่ห่างไกลกันนับหมื่นกิโลเมตร เข้าเป็นหนึ่งเดียวในครอบครัว:</p>
      <ul style="line-height:1.7;">
        <li><strong>สายตระกูลทางฝั่งมารดา (ประเทศไทย แถบชายฝั่งอ่าวไทย):</strong> สายนามสกุลเก่าแก่แห่งเมืองชุมพร ได้แก่ <strong>พิทักษ์ (Pithak)</strong>, <strong>ป่าไม้ทอง (Pamaitong)</strong> และ <strong>ชำนาญการ (Chamniankan)</strong> โดยมีคุณทวดสาย ป่าไม้ทอง (เกิด พ.ศ. 2462), คุณยายดวงเดือน ป่าไม้ทอง (เกิด พ.ศ. 2504) และคุณแม่ปริตา (พิทักษ์) เตอร์คิน (เกิด พ.ศ. 2540)</li>
        <li><strong>สายตระกูลทางฝั่งบิดา (สาธารณรัฐโคมิ สหพันธรัฐรัสเซีย ดินแดนทางตอนเหนือ):</strong> สายตระกูลดั้งเดิมของชนชาติโคมิ-ซีเรียน (Komi-Zyryan) 4 สายหลักจากลุ่มแม่น้ำวิเชกดะและวิม สายเลือดสายตรงฝ่ายชายของตระกูลเตอร์คินได้รับการยืนยันด้วยเอกสารประวัติศาสตร์ของรัฐรัสเซียอย่างต่อเนื่องยาวนานถึง 15 ชั่วคน ย้อนกลับไปถึงปี ค.ศ. 1608 (พ.ศ. 2151 ในรัชสมัยกรุงศรีอยุธยา รวมกว่า 416 ปีแห่งประวัติศาสตร์ที่มีหลักฐานยืนยัน) พร้อมด้วยสายตระกูลเชโคนิน, ชุกโตมอฟ, ซิโนเวียฟ และเลทอฟ ซึ่งสืบสาวกลับไปได้ถึงคริสต์ศตวรรษที่ 17–18</li>
      </ul>
    </div>"""

    # 2. Heroes Card
    thai_heroes_card = get_thai_heroes_html()

    # 3. Clergy Card
    thai_clergy_card = get_thai_clergy_html()

    # 4. Court Battles & State Service Card
    thai_court_card = get_thai_court_html()

    # 5. Build Thai Geography Cards (14 villages)
    geo = THAI_TRANSLATIONS_ALL["geo"]
    geo_keys = [
        'yb', 'gorely_yb', 'loyma', 'erozdino', 'vogvazdino', 'lyali', 'paltydor',
        'kokvitsy', 'okvad', 'ust_vym', 'syulatuy', 'syktyvkar', 'ulyanovo', 'chumphon'
    ]

    colors = {
        'yb': 'var(--accent)', 'gorely_yb': '#ec4899', 'loyma': '#8b5cf6', 'erozdino': '#d97706',
        'vogvazdino': '#059669', 'lyali': '#d97706', 'paltydor': '#2563eb', 'kokvitsy': '#2563eb',
        'okvad': '#2563eb', 'ust_vym': '#059669', 'syulatuy': '#2563eb', 'syktyvkar': '#059669',
        'ulyanovo': '#4f46e5', 'chumphon': '#10b981'
    }

    new_geo_cards = []
    for k in geo_keys:
        d = geo[k]
        col = colors.get(k, 'var(--accent)')
        if k == 'ulyanovo':
            c_html = f"""        <!-- УЛЬЯНОВО И КУЖБА -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:{col}; margin-bottom:0.35rem;">{d['title']}</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">{d['sub']}</div>
          <p style="font-size:0.86rem; line-height:1.6; margin-bottom:0.75rem;">{d['text']}</p>

          <!-- ВЫДЕЛЕННЫЙ БЛОК: НОВОМУЧЕНИК МЕЛЕТИЙ -->
          <div style="background:linear-gradient(135deg, rgba(124,58,237,0.06), rgba(217,119,6,0.06)); border:1.5px solid rgba(124,58,237,0.25); border-radius:8px; padding:0.65rem 0.75rem; display:flex; gap:0.75rem; align-items:flex-start;">
            <div onclick="openFullscreenScan('архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg', 'Преподобномученик МЕЛЕТИЙ иеромонах', 'Казначей Троице-Стефано-Ульяновского монастыря, преподобномученик Мелетий (Федюнёв)')" title="คลิกเพื่อดูรูปขนาดใหญ่" style="cursor:pointer; flex:0 0 92px; text-align:center;">
              <img src="архив_сканы_первоисточников/Преподобномученик_Мелетий_Федюнев.jpg" alt="พระมรณสักขี เมเลตี" style="width:92px; height:118px; object-fit:cover; border-radius:6px; border:1.5px solid #7c3aed; box-shadow:0 2px 5px rgba(0,0,0,0.15); display:block; transition:transform 0.2s; margin:0 auto;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='scale(1)'" />
              <div style="font-size:0.64rem; font-weight:700; color:#6d28d9; margin-top:0.35rem; width:100%; line-height:1.2;">พระเมเลตี<br><span style="font-size:0.60rem; font-weight:600; color:var(--text-muted);">(เฟดิวเนียฟ)</span></div>
            </div>
            <div style="font-size:0.79rem; line-height:1.5; color:var(--text-main);">
              <div style="font-weight:700; color:#6d28d9; margin-bottom:0.2rem; font-size:0.82rem;">{d['meletiy_title']}</div>
              <div>{d['meletiy_body']}</div>
            </div>
          </div>

          <div style="margin-top:0.75rem; padding-top:0.5rem; border-top:1px dashed var(--border-color); display:flex; gap:0.4rem;">
            <button class="pill-btn" onclick="focusPerson('I307'); switchTab('tree');" style="font-size:0.74rem;">🎯 พระภิกษุวิตาลี (เตอร์คิน)</button>
          </div>
        </div>"""
        else:
            c_html = f"""        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:{col}; margin-bottom:0.35rem;">{d['title']}</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">{d['sub']}</div>
          <p style="font-size:0.86rem; line-height:1.6;">{d['text']}</p>
        </div>"""
        new_geo_cards.append(c_html)

    new_geo_cards_str = '\n\n'.join(new_geo_cards)

    thai_geography_card = f"""    <!-- GEOGRAPHY SECTION -->
    <div class="info-card" id="info-geography">
      <h2>{THAI_TRANSLATIONS_ALL["geo_heading"]}</h2>
      <p style="color:var(--text-muted); margin-bottom:1.25rem;">{THAI_TRANSLATIONS_ALL["geo_lead"]}</p>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">
{new_geo_cards_str}
      </div>
    </div>"""

    # 6. Build Thai Surnames Cards (18 surnames)
    sur = THAI_TRANSLATIONS_ALL["sur"]
    sur_keys = [
        ('turkin', '#2563eb'), ('letov', '#2563eb'), ('yaranov', '#2563eb'), ('sizev', '#2563eb'),
        ('syutkin', '#8b5cf6'), ('shekhonin', '#8b5cf6'), ('shuktomov', '#d97706'), ('poleshchikov', '#d97706'),
        ('pasynkov', '#d97706'), ('kruglyakov', '#d97706'), ('zinoviev', '#ec4899'), ('pozdeev', '#ec4899'),
        ('kyzyurov', '#ec4899'), ('aibabin', '#ec4899'), ('karakchiev', '#ec4899'), ('pithak', '#10b981'),
        ('pamaitong', '#10b981'), ('chamniankan', '#10b981')
    ]

    new_sur_cards = []
    for k, col in sur_keys:
        d = sur[k]
        c_html = f"""        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:{col}; font-size:0.98rem;">{d['name']}</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:rgba(0,0,0,0.04); color:{col}; border-radius:4px; font-weight:700;">{d['badge']}</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.6;">{d['text']}</p>
        </div>"""
        new_sur_cards.append(c_html)

    new_sur_cards_str = '\n\n'.join(new_sur_cards)

    thai_surnames_card = f"""    <!-- ONOMASTICS AND SURNAMES SECTION -->
    <div class="info-card" id="info-surnames">
      <h2>{THAI_TRANSLATIONS_ALL["sur_heading"]}</h2>
      <p style="color:var(--text-muted); margin-bottom:1.25rem;">{THAI_TRANSLATIONS_ALL["sur_lead"]}</p>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1rem;">
{new_sur_cards_str}
      </div>
    </div>"""

    # 7. Complete 6-item Bottom Anchor Bar (Identical to Russian version)
    thai_bottom_bar = """    <!-- BOTTOM ANCHOR NAVIGATION BAR FOR PLACES & ROOTS -->
    <nav class="info-bottom-bar" id="infoBottomBar">
      <div class="info-bottom-scroll">
        <a href="#info-overview" class="info-bottom-pill active" onclick="scrollToAnchor(event, 'info-overview')" title="เกี่ยวกับตระกูล (О семье)">
          <span>🌳</span> <span class="pill-lbl-full">О семье</span><span class="pill-lbl-short">Семья</span>
        </a>
        <a href="#info-heroes" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-heroes')" title="ผู้พิทักษ์ปิตุภูมิ / วีรชน (Защитники)">
          <span>🎖️</span> <span class="pill-lbl-full">Защитники</span><span class="pill-lbl-short">Герои</span>
        </a>
        <a href="#info-clergy" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-clergy')" title="คณะสงฆ์และวัดวาอาราม (Духовенство)">
          <span>⛪</span> <span class="pill-lbl-full">Духовенство</span><span class="pill-lbl-short">Храмы</span>
        </a>
        <a href="#info-court-cases" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-court-cases')" title="การรับราชการและคดีความ (Служба)">
          <span>⚖️</span> <span>Служба</span>
        </a>
        <a href="#info-geography" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-geography')" title="ภูมิศาสตร์ประวัติศาสตร์ (География)">
          <span>🗺️</span> <span class="pill-lbl-full">География</span><span class="pill-lbl-short">Места</span>
        </a>
        <a href="#info-surnames" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-surnames')" title="สายตระกูลและนามสกุล (Фамилии)">
          <span>🧬</span> <span class="pill-lbl-full">Фамилии</span><span class="pill-lbl-short">Роды</span>
        </a>
      </div>
    </nav>"""

    # 8. Assemble entire Thai view-info
    new_view_info = f"""<div id="view-info" class="view-section active">
{thai_overview_card}

{thai_heroes_card}

{thai_clergy_card}

{thai_court_card}

{thai_geography_card}

{thai_surnames_card}

{thai_bottom_bar}
  </div>"""

    # 9. Safely replace view-info BEFORE any other string manipulations
    start_tag = '<div id="view-info" class="view-section">'
    end_tag = '<!-- TAB 6: SOURCES AND BIBLIOGRAPHY VIEW -->'
    start_info = html.find(start_tag)
    end_info = html.find(end_tag, start_info)
    assert start_info != -1 and end_info != -1, "view-info section boundary not found!"

    # Replace view-info cleanly
    html = html[:start_info] + new_view_info + '\n\n  ' + html[end_info:]

    # 10. Page Title and Google Font Sarabun
    thai_font_links = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
</head>"""
    html = html.replace('</head>', thai_font_links, 1)

    html = html.replace(
        '<title>Родословная Туркиных</title>',
        '<title>สาแหรกตระกูลเตอร์คิน (ตูร์กิน) • ตระกูลพิทักษ์ • ลำดับญาติ 20 ชั่วคน</title>'
    )
    html = html.replace(
        '<h1>Родословная Туркиных</h1>',
        '<h1>สาแหรกตระกูลเตอร์คิน (ตูร์กิน)</h1>'
    )
    html = html.replace(
        '>20 поколений • 332 персон<',
        '>ลำดับญาติ 20 ชั่วคน • 332 บุคคล<'
    )

    # 11. Header and Drawer language buttons (switch back to Russian)
    desktop_th_btn = '<a href="thai.html" class="pill-btn" style="text-decoration:none; font-weight:600; font-size:0.78rem; padding:0.25rem 0.6rem; background:rgba(16,185,129,0.08); border-color:#10b981; color:#059669;" title="หน้าภาษาไทย">🇹🇭 ภาษาไทย</a>'
    desktop_ru_btn = '<a href="index.html" class="pill-btn" style="text-decoration:none; font-weight:600; font-size:0.78rem; padding:0.25rem 0.6rem; background:rgba(37,99,235,0.08); border-color:#2563eb; color:#2563eb;" title="กลับไปหน้าภาษารัสเซีย">🇷🇺 Версия на русском</a>'
    html = html.replace(desktop_th_btn, desktop_ru_btn)

    mobile_th_btn = '<a href="thai.html" class="pill-btn" style="text-decoration:none; font-size:0.78rem; padding:0.3rem 0.7rem; color:#059669; border-color:#10b981; background:rgba(16,185,129,0.08);">🇹🇭 ภาษาไทย</a>'
    mobile_ru_btn = '<a href="index.html" class="pill-btn" style="text-decoration:none; font-size:0.78rem; padding:0.3rem 0.7rem; color:#2563eb; border-color:#2563eb; background:rgba(37,99,235,0.08);" title="กลับไปหน้าภาษารัสเซีย">🇷🇺 Русский</a>'
    html = html.replace(mobile_th_btn, mobile_ru_btn)

    # 12. Nav tabs translation & setting default active tab to 'info'
    html = html.replace(
        '<button class="nav-tab active" onclick="switchTab(\'tree\')">🌿 Древо</button>',
        '<button class="nav-tab" onclick="switchTab(\'tree\')">🌿 สาแหรกต้นไม้</button>'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'list\')">📜 Поколения</button>',
        '<button class="nav-tab" onclick="switchTab(\'list\')">📜 ลำดับรุ่น</button>'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'table\')">📋 Таблица</button>',
        '<button class="nav-tab" onclick="switchTab(\'table\')">📋 สารบัญรายชื่อ</button>'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'archive\')">🏛️ Архив документов',
        '<button class="nav-tab" onclick="switchTab(\'archive\')">🏛️ หอจดหมายเหตุ'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'info\')">🗺️ Места и роды</button>',
        '<button class="nav-tab active" onclick="switchTab(\'info\')">🗺️ ถิ่นกำเนิดและสายตระกูล</button>'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'sources\')">📚 Источники</button>',
        '<button class="nav-tab" onclick="switchTab(\'sources\')">📚 เอกสารอ้างอิง</button>'
    )
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'stats\')">📊 Статистика</button>',
        '<button class="nav-tab" onclick="switchTab(\'stats\')">📊 สถิติตระกูล</button>'
    )

    # In HTML, view-tree was originally active; make it inactive by default so only view-info is active
    html = html.replace(
        '<div id="view-tree" class="view-section active">',
        '<div id="view-tree" class="view-section">'
    )

    # Drawer menu items
    html = html.replace('<span>Интерактивное древо</span>', '<span>สาแหรกต้นไม้</span>')
    html = html.replace('<span>Список поколений</span>', '<span>ลำดับรุ่น</span>')
    html = html.replace('<span>Таблица персон</span>', '<span>สารบัญรายชื่อ</span>')
    html = html.replace('<span>Архив первоисточников</span>', '<span>หอจดหมายเหตุ</span>')
    html = html.replace('<span>Места и роды</span>', '<span>ถิ่นกำเนิดและสายตระกูล</span>')
    html = html.replace('<span>Источники и литература</span>', '<span>เอกสารอ้างอิง</span>')
    html = html.replace('<span>Статистика рода</span>', '<span>สถิติตระกูล</span>')
    html = html.replace('<span>☰</span> <span>Меню</span>', '<span>☰</span> <span>เมนู</span>')
    html = html.replace('placeholder="Поиск персоны..."', 'placeholder="ค้นหาบุคคลในตระกูล..."')

    # 13. Add Thai body font styling
    html = html.replace('<body>', '<body style="font-family: \'Sarabun\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; line-height: 1.6;">')

    # 14. Set default tab to 'info' on load if no specific hash provided
    html = html.replace(
        'setupHashRouting();\n}',
        'setupHashRouting();\n  if (!window.location.hash) switchTab(\'info\');\n}'
    )

    with open('thai.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('SUCCESS: thai.html generated with 100% complete Thai version of all 6 sections!')

if __name__ == '__main__':
    build_thai_file()
