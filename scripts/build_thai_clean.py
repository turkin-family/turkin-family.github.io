#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_thai_clean.py
Generates thai.html from index.html with idiomatic Thai translation
for the "Places and Roots" (ถิ่นกำเนิดและสายตระกูล) section.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.thai_translations_all import THAI_TRANSLATIONS_ALL

def build_thai_file():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Page Title and Google Font Sarabun
    thai_font_links = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
</head>"""
    html = html.replace('</head>', thai_font_links)

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

    # 2. Header and Drawer language buttons (switch to Russian)
    desktop_th_btn = '<a href="thai.html" class="pill-btn" style="text-decoration:none; font-weight:600; font-size:0.78rem; padding:0.25rem 0.6rem; background:rgba(16,185,129,0.08); border-color:#10b981; color:#059669;" title="หน้าภาษาไทย">🇹🇭 ภาษาไทย</a>'
    desktop_ru_btn = '<a href="index.html" class="pill-btn" style="text-decoration:none; font-weight:600; font-size:0.78rem; padding:0.25rem 0.6rem; background:rgba(37,99,235,0.08); border-color:#2563eb; color:#2563eb;" title="กลับไปหน้าภาษารัสเซีย">🇷🇺 Версия на русском</a>'
    html = html.replace(desktop_th_btn, desktop_ru_btn)

    mobile_th_btn = '<a href="thai.html" class="pill-btn" style="text-decoration:none; font-size:0.78rem; padding:0.3rem 0.7rem; color:#059669; border-color:#10b981; background:rgba(16,185,129,0.08);">🇹🇭 ภาษาไทย</a>'
    mobile_ru_btn = '<a href="index.html" class="pill-btn" style="text-decoration:none; font-size:0.78rem; padding:0.3rem 0.7rem; color:#2563eb; border-color:#2563eb; background:rgba(37,99,235,0.08);" title="กลับไปหน้าภาษารัสเซีย">🇷🇺 Русский</a>'
    html = html.replace(mobile_th_btn, mobile_ru_btn)

    # 3. Nav tabs label
    html = html.replace(
        '<button class="nav-tab" onclick="switchTab(\'info\')">🗺️ Места и роды</button>',
        '<button class="nav-tab" onclick="switchTab(\'info\')">🗺️ ถิ่นกำเนิดและสายตระกูล</button>'
    )
    html = html.replace(
        '<span class="drawer-nav-icon">🗺️</span>\n        <span>Места и роды</span>',
        '<span class="drawer-nav-icon">🗺️</span>\n        <span>ถิ่นกำเนิดและสายตระกูล</span>'
    )

    # 4. Headings in info-geography & info-surnames
    html = html.replace(
        '<h2>🗺️ Историческая география селений и городов рода</h2>',
        f'<h2>{THAI_TRANSLATIONS_ALL["geo_heading"]}</h2>'
    )
    html = html.replace(
        '<p style="color:var(--text-muted); margin-bottom:1.25rem;">Селения расположены в бассейнах великих рек Русского Севера (Сысолы, Вычегды, Выми, Лузы) и на юге Сиама:</p>',
        f'<p style="color:var(--text-muted); margin-bottom:1.25rem;">{THAI_TRANSLATIONS_ALL["geo_lead"]}</p>'
    )
    html = html.replace(
        '<h2>🧬 Происхождение фамилий и история родов</h2>',
        f'<h2>{THAI_TRANSLATIONS_ALL["sur_heading"]}</h2>'
    )
    html = html.replace(
        '<p style="color:var(--text-muted); margin-bottom:1.25rem;">Ономастическое исследование коми и тайских родовых имен, вошедших в родословную:</p>',
        f'<p style="color:var(--text-muted); margin-bottom:1.25rem;">{THAI_TRANSLATIONS_ALL["sur_lead"]}</p>'
    )

    # 5. Extract and replace Geography section
    geo = THAI_TRANSLATIONS_ALL["geo"]
    geo_keys = [
        'yb', 'gorely_yb', 'loyma', 'erozdino', 'vogvazdino', 'lyali', 'paltydor',
        'kokvitsy', 'okvad', 'ust_vym', 'syulatuy', 'syktyvkar', 'ulyanovo', 'chumphon'
    ]

    # Find geography cards block
    start_grid = html.find('<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">')
    end_grid = html.find('</div>\n    </div>\n\n    <!-- ONOMASTICS AND SURNAMES SECTION -->', start_grid)
    assert start_grid != -1 and end_grid != -1, "Geography grid block not found in index.html!"

    new_geo_cards = []
    colors = {
        'yb': 'var(--accent)', 'gorely_yb': '#ec4899', 'loyma': '#8b5cf6', 'erozdino': '#d97706',
        'vogvazdino': '#059669', 'lyali': '#d97706', 'paltydor': '#2563eb', 'kokvitsy': '#2563eb',
        'okvad': '#2563eb', 'ust_vym': '#059669', 'syulatuy': '#2563eb', 'syktyvkar': '#059669',
        'ulyanovo': '#4f46e5', 'chumphon': '#10b981'
    }

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
        </div>"""
        else:
            c_html = f"""        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:{col}; margin-bottom:0.35rem;">{d['title']}</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">{d['sub']}</div>
          <p style="font-size:0.86rem; line-height:1.6;">{d['text']}</p>
        </div>"""
        new_geo_cards.append(c_html)

    new_geo_grid = '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">\n' + '\n\n'.join(new_geo_cards) + '\n      '
    html = html[:start_grid] + new_geo_grid + html[end_grid:]

    # 6. Extract and replace Surnames section
    sur = THAI_TRANSLATIONS_ALL["sur"]
    sur_keys = [
        ('turkin', '#2563eb'), ('letov', '#2563eb'), ('yaranov', '#2563eb'), ('sizev', '#2563eb'),
        ('syutkin', '#8b5cf6'), ('shekhonin', '#8b5cf6'), ('shuktomov', '#d97706'), ('poleshchikov', '#d97706'),
        ('pasynkov', '#d97706'), ('kruglyakov', '#d97706'), ('zinoviev', '#ec4899'), ('pozdeev', '#ec4899'),
        ('kyzyurov', '#ec4899'), ('aibabin', '#ec4899'), ('karakchiev', '#ec4899'), ('pithak', '#10b981'),
        ('pamaitong', '#10b981'), ('chamniankan', '#10b981')
    ]

    start_sur_grid = html.find('<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1rem;">')
    end_sur_grid = html.find('</div>\n    </div>\n\n    <!-- BOTTOM ANCHOR NAVIGATION BAR FOR PLACES & ROOTS -->', start_sur_grid)
    assert start_sur_grid != -1 and end_sur_grid != -1, "Surnames grid block not found in index.html!"

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

    new_sur_grid = '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1rem;">\n' + '\n\n'.join(new_sur_cards) + '\n      '
    html = html[:start_sur_grid] + new_sur_grid + html[end_sur_grid:]

    # 7. Add Thai body font styling
    html = html.replace('<body>', '<body style="font-family: \'Sarabun\', -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; line-height: 1.6;">')

    # 8. Set default tab to 'info' on load if no specific hash provided
    html = html.replace(
        'setupHashRouting();\n}',
        'setupHashRouting();\n  if (!window.location.hash) switchTab(\'info\');\n}'
    )

    with open('thai.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('SUCCESS: thai.html generated with 100% precision!')

if __name__ == '__main__':
    build_thai_file()
