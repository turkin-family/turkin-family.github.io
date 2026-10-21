# -*- coding: utf-8 -*-
import json
import build_genealogy
import archive_catalog

persons = build_genealogy.persons
families = build_genealogy.families
person_dict = {p['id']: p for p in persons}
family_dict = {f['id']: f for f in families}

# 1. Verification of user corrections
for p in persons:
    for n in p.get('notes', []):
        assert 'Ларита' not in n, f"Found 'Ларита' in {p['id']}"
        assert 'Глаголева' not in n, f"Found 'Глаголева' in {p['id']}"
        assert 'Лёк' not in n, f"Found 'Лёк' in {p['id']}"
        assert 'Лекина' not in n, f"Found 'Лекина' in {p['id']}"
        assert 'Легов' not in n, f"Found 'Легов' in {p['id']}"
        assert 'Чулымск' not in n, f"Found 'Чулымск' in {p['id']}"

assert person_dict['I1']['birt_plac'] == 'г. Чумпхон (Таиланд)'
assert person_dict['I3']['name'] == 'Парита (Питак) /Туркина/'
assert person_dict['I16']['name'] == 'Альбина Семеновна (Зиновьева) /Гладышева/'
assert person_dict['I52']['name'] == 'Пётр /Сюткин/'
assert person_dict['I29']['name'] == 'Савватий Васильевич /Летов/'
assert person_dict['I19']['birt_plac'] == 'с. Коквицы'
assert person_dict['I13']['birt_plac'] == 'с. Коквицы'
assert person_dict['I67']['name'] == 'Владимир Семенович /Зиновьев/'

# 2. Assign generation to each person
ancient_seeds = {
    'I1': 1,
    'I70': 8,
    'I148': 9,
    'I80': 10,
    'I79': 10,
    'I77': 10,
    'I78': 11,
    'I75': 11,
    'I71': 12,
    'I72': 13,
    'I73': 14,
    'I74': 15,
}
gen_map = dict(ancient_seeds)
changed = True
while changed:
    changed = False
    for f in families:
        children = f.get('children', [])
        husb = f.get('husb')
        wife = f.get('wife')
        
        # 1. Снизу вверх: от детей к родителям (родитель = ребенок + 1)
        for c in children:
            if c in gen_map:
                cg = gen_map[c]
                if husb and (husb not in gen_map or gen_map[husb] < cg + 1):
                    gen_map[husb] = cg + 1
                    changed = True
                if wife and (wife not in gen_map or gen_map[wife] < cg + 1):
                    gen_map[wife] = cg + 1
                    changed = True
                    
        # 2. Горизонтально между сиблингами
        gens = [gen_map[c] for c in children if c in gen_map]
        if gens:
            mg = max(gens)
            for c in children:
                if c not in gen_map or gen_map[c] < mg:
                    gen_map[c] = mg
                    changed = True
                    
        # 3. Сверху вниз: от родителей к детям (дети = родитель - 1)
        pgens = [gen_map[p] for p in [husb, wife] if p and p in gen_map]
        if pgens:
            exp_cgen = min(pgens) - 1
            for c in children:
                if c == 'I70':
                    continue
                if c not in gen_map or gen_map[c] != exp_cgen:
                    gen_map[c] = exp_cgen
                    changed = True

for f in families:
    husb = f.get('husb')
    wife = f.get('wife')
    if husb and wife:
        if husb in gen_map and wife not in gen_map:
            gen_map[wife] = gen_map[husb]
        elif wife in gen_map and husb not in gen_map:
            gen_map[husb] = gen_map[wife]

import re
def _parse_yr(s):
    if not s: return None
    m = re.search(r'\b(1[6789]\d{2}|20\d{2})\b', s)
    return int(m.group(1)) if m else None

for p in persons:
    pid = p['id']
    if pid not in gen_map:
        if p.get('gen'):
            gen_map[pid] = p['gen']
        else:
            yr = _parse_yr(p.get('birt_date')) or (_parse_yr(p.get('deat_date')) - 50 if _parse_yr(p.get('deat_date')) else None)
            if yr:
                gen_map[pid] = max(1, min(15, round((1995 - yr) / 30) + 1))
            else:
                gen_map[pid] = 7

changed = True
while changed:
    changed = False
    for f in families:
        children = f.get('children', [])
        husb = f.get('husb')
        wife = f.get('wife')
        for c in children:
            if c in gen_map:
                cg = gen_map[c]
                if husb and (husb not in gen_map or gen_map[husb] < cg + 1):
                    gen_map[husb] = cg + 1
                    changed = True
                if wife and (wife not in gen_map or gen_map[wife] < cg + 1):
                    gen_map[wife] = cg + 1
                    changed = True
        pgens = [gen_map[p] for p in [husb, wife] if p and p in gen_map]
        if pgens:
            exp_cgen = min(pgens) - 1
            for c in children:
                if c == 'I70': continue
                if c not in gen_map or gen_map[c] != exp_cgen:
                    gen_map[c] = exp_cgen
                    changed = True
        if husb and wife:
            if husb in gen_map and wife not in gen_map:
                gen_map[wife] = gen_map[husb]
                changed = True
            elif wife in gen_map and husb not in gen_map:
                gen_map[husb] = gen_map[wife]
                changed = True

for pid, g in ancient_seeds.items():
    gen_map[pid] = g

for p in persons:
    p['gen'] = gen_map.get(p['id'], p.get('gen', 1))

def format_gedcom_date(d):
    if not d:
        return ""
    d_clean = d.strip()
    if d_clean.upper().startswith("ABT "):
        rest = format_gedcom_date(d_clean[4:])
        return f"ок. {rest}"
    if d_clean.upper().startswith("BEF "):
        rest = format_gedcom_date(d_clean[4:])
        return f"до {rest}"
    if d_clean.upper().startswith("AFT "):
        rest = format_gedcom_date(d_clean[4:])
        return f"после {rest}"
    if any(d_clean.lower().startswith(pfx) for pfx in ['ок.', 'ок', 'до', 'после', 'около', '~']):
        return d_clean
    months = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    parts = d_clean.split()
    if len(parts) == 3:
        day, mon, yr = parts
        if mon.upper() in months:
            return f"{day.zfill(2)}.{months[mon.upper()]}.{yr}"
    elif len(parts) == 2:
        mon, yr = parts
        if mon.upper() in months:
            return f"{months[mon.upper()]}.{yr}"
    elif len(parts) == 1:
        return parts[0]
    return d_clean

for p in persons:
    p['display_birt'] = format_gedcom_date(p.get('birt_date'))
    p['display_deat'] = format_gedcom_date(p.get('deat_date'))
    clean_name = p['name'].replace('/', '').strip()
    p['clean_name'] = clean_name
    p['father_id'] = None
    p['mother_id'] = None
    p['spouses'] = []
    p['children_ids'] = []
    p['siblings_ids'] = []

for f in families:
    husb = f.get('husb')
    wife = f.get('wife')
    children = f.get('children', [])
    marr = f.get('marr_date')
    if husb and wife:
        person_dict[husb]['spouses'].append({'id': wife, 'marr_date': marr})
        person_dict[wife]['spouses'].append({'id': husb, 'marr_date': marr})
    for c in children:
        cp = person_dict[c]
        if husb:
            cp['father_id'] = husb
            if c not in person_dict[husb]['children_ids']:
                person_dict[husb]['children_ids'].append(c)
        if wife:
            cp['mother_id'] = wife
            if c not in person_dict[wife]['children_ids']:
                person_dict[wife]['children_ids'].append(c)
        for other_c in children:
            if other_c != c and other_c not in cp['siblings_ids']:
                cp['siblings_ids'].append(other_c)

import layout_engine

layout_engine.assign_branch_info(persons)
gen_x = layout_engine.GEN_X
coords = layout_engine.compute_smart_layout(persons, families)

for pid, (x, y) in coords.items():
    if pid in person_dict:
        person_dict[pid]['x'] = x
        person_dict[pid]['y'] = y

for p in persons:
    if 'x' not in p or 'y' not in p:
        gx = gen_x.get(p.get('gen', 1), 80)
        p['x'] = gx
        p['y'] = 800
        print(f"Assigned fallback coords to {p['id']}: ({p['x']}, {p['y']})")

total_persons = len(persons)
male_count = sum(1 for p in persons if p['sex'] == 'M')
female_count = sum(1 for p in persons if p['sex'] == 'F')
total_families = len(families)
max_gen = max(p['gen'] for p in persons)

max_coord_x = max(p['x'] for p in persons) + 380
max_coord_y = max(p['y'] for p in persons) + 380
canvas_w = max(7700, max_coord_x)
canvas_h = max(3600, max_coord_y)

indis_json = json.dumps(person_dict, ensure_ascii=False)
fams_json = json.dumps(families, ensure_ascii=False)
docs_json = json.dumps(archive_catalog.DOCS_CATALOG, ensure_ascii=False)
pdfs_json = json.dumps(archive_catalog.PDF_ALBUMS, ensure_ascii=False)

yandex_metrika_code = '''<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=113692901', 'ym');

    ym(113692901, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/113692901" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->'''

html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Родословное древо семьи Туркиных</title>
{yandex_metrika_code}
<style>
:root {{
  --bg-primary: #f8fafc;
  --bg-surface: #ffffff;
  --bg-card: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border-color: #cbd5e1;
  --accent: #2563eb;
  --accent-light: #eff6ff;
  --male-border: #3b82f6;
  --male-bg: #eff6ff;
  --female-border: #ec4899;
  --female-bg: #fdf2f8;
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.08);
  --shadow-lg: 0 10px 20px -3px rgb(0 0 0 / 0.12), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --radius: 8px;
}}

[data-theme="dark"] {{
  --bg-primary: #0b0f19;
  --bg-surface: #111827;
  --bg-card: #1f293d;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --border-color: #334155;
  --accent: #38bdf8;
  --accent-light: #1e293b;
  --male-border: #60a5fa;
  --male-bg: #1e293b;
  --female-border: #f472b6;
  --female-bg: #2d1828;
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
  --shadow-lg: 0 10px 20px -3px rgb(0 0 0 / 0.5);
}}

html, body {{
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}}

* {{ box-sizing: border-box; }}

body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-main);
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
}}

/* FIXED TOP HEADER (NEVER WRAPS, ALWAYS VISIBLE AT ANY ZOOM) */
header {{
  flex: 0 0 54px;
  height: 54px;
  min-height: 54px;
  max-height: 54px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  z-index: 1000;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}

.brand {{
  display: flex;
  align-items: center;
  gap: 0.55rem;
  flex-shrink: 0;
}}
.brand-icon {{
  font-size: 1.6rem;
  line-height: 1;
}}
.brand-text {{
  display: flex;
  flex-direction: column;
  justify-content: center;
}}
.brand-text h1 {{
  margin: 0;
  padding: 0;
  font-size: 1.05rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.01em;
  white-space: nowrap;
}}
.brand-badge {{
  font-size: 0.7rem;
  line-height: 1.1;
  color: var(--text-muted);
  font-weight: 500;
  white-space: nowrap;
  margin-top: 2px;
}}

/* NAVIGATION TABS */
.nav-tabs {{
  display: flex;
  background: var(--bg-primary);
  padding: 0.18rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}}
.nav-tab {{
  padding: 0.35rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-muted);
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  white-space: nowrap;
}}
.nav-tab.active {{
  background: var(--bg-surface);
  color: var(--accent);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}

/* HEADER RIGHT CONTROLS */
.header-right {{
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-shrink: 0;
}}
.search-box {{
  position: relative;
  display: flex;
  align-items: center;
}}
.search-box input {{
  padding: 0.35rem 0.65rem 0.35rem 1.75rem;
  font-size: 0.8rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-main);
  outline: none;
  width: 170px;
  transition: width 0.2s ease, border-color 0.2s ease;
}}
.search-box input:focus {{
  width: 210px;
  border-color: var(--accent);
}}
.search-icon {{
  position: absolute;
  left: 0.5rem;
  font-size: 0.78rem;
  color: var(--text-muted);
}}

.btn-icon {{
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-main);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.15s ease;
}}
.btn-icon:hover {{
  background: var(--accent-light);
  border-color: var(--accent);
}}

/* MAIN CONTENT CONTAINER */
main {{
  flex: 1 1 0;
  min-height: 0;
  position: relative;
  overflow: hidden;
  width: 100%;
}}

.view-section {{
  display: none;
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0;
}}
.view-section.active {{
  display: block;
}}

/* TREE VIEW */
#view-tree {{
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  cursor: grab;
  user-select: none;
  background-color: var(--bg-primary);
  background-image: radial-gradient(var(--border-color) 1px, transparent 1px);
  background-size: 28px 28px;
}}
#view-tree:active {{ cursor: grabbing; }}

/* TREE SUB-TOOLBAR (IN TREE VIEW) */
.tree-subbar {{
  position: absolute;
  top: 0.65rem;
  left: 0.85rem;
  right: 0.85rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  z-index: 100;
  pointer-events: none;
}}
.tree-subbar-left, .tree-subbar-right {{
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.25rem 0.45rem;
  box-shadow: var(--shadow);
  pointer-events: auto;
  backdrop-filter: blur(8px);
}}

.subbar-label {{
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-right: 0.2rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}

.pill-btn {{
  padding: 0.22rem 0.55rem;
  border-radius: 5px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-main);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.15s ease;
  white-space: nowrap;
}}
.pill-btn:hover {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}
.pill-btn.active {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}

.subbar-btn {{
  padding: 0.22rem 0.55rem;
  border-radius: 5px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-main);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.15s ease;
  white-space: nowrap;
}}
.subbar-btn:hover {{
  background: var(--accent-light);
  border-color: var(--accent);
}}
.subbar-btn.active {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}

/* PINNED GENERATION BAR (ALWAYS AT TOP, TRANSLATES WITH PANX) */
.pinned-gen-bar {{
  position: absolute;
  top: 42px;
  left: 0;
  width: 100%;
  height: 28px;
  z-index: 50;
  pointer-events: none;
  overflow: hidden;
}}
.pinned-gen-track {{
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: {canvas_w}px;
  transform-origin: 0 0;
}}
.pinned-gen-title {{
  position: absolute;
  top: 0;
  width: 240px;
  padding: 0.2rem 0.4rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  text-align: center;
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--text-muted);
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: auto;
  cursor: pointer;
  transition: all 0.15s ease;
}}
.pinned-gen-title:hover {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.25);
}}
.pinned-gen-title.active-gen {{
  background: var(--accent) !important;
  color: #fff !important;
  border-color: var(--accent) !important;
  box-shadow: 0 0 14px rgba(56, 189, 248, 0.75) !important;
}}

/* CANVAS & LAYERS */
.tree-canvas {{
  position: absolute;
  top: 0;
  left: 0;
  transform-origin: 0 0;
  width: {canvas_w}px;
  height: {canvas_h}px;
  transition: transform 0.05s linear;
}}

#treeSvg {{
  position: absolute;
  top: 0;
  left: 0;
  width: {canvas_w}px;
  height: {canvas_h}px;
  pointer-events: none;
  z-index: 20;
  overflow: visible;
}}

.tree-link {{
  fill: none;
  stroke-linecap: round;
  transition: stroke 0.2s ease, stroke-width 0.2s ease, opacity 0.2s ease;
}}
.tree-link.link-father {{
  stroke: #2563eb;
  stroke-width: 2.5px;
  stroke-opacity: 0.75;
}}
.tree-link.link-mother {{
  stroke: #db2777;
  stroke-width: 2.5px;
  stroke-opacity: 0.75;
}}
.tree-link.link-spouse {{
  stroke: #8b5cf6;
  stroke-width: 2px;
  stroke-dasharray: 5 4;
  stroke-opacity: 0.8;
}}
.tree-link.link-research {{
  stroke: #a855f7;
  stroke-width: 2.5px;
  stroke-dasharray: 6 5;
  stroke-opacity: 0.85;
}}

.flow-active .tree-link {{
  stroke-dasharray: 8 6;
  animation: flowLine 1.5s linear infinite;
}}
@keyframes flowLine {{
  to {{ stroke-dashoffset: -28; }}
}}

.tree-link.highlighted {{
  stroke: #f59e0b !important;
  stroke-width: 4px !important;
  stroke-opacity: 1 !important;
  filter: drop-shadow(0 0 4px rgba(245, 158, 11, 0.6));
  z-index: 20;
}}
.tree-link.dimmed {{
  stroke-opacity: 0.12 !important;
}}

#cardsLayer {{
  position: absolute;
  top: 0;
  left: 0;
  width: {canvas_w}px;
  height: {canvas_h}px;
  z-index: 15;
  pointer-events: none;
}}

.person-card {{
  position: absolute;
  width: 246px;
  height: 78px;
  background: var(--bg-card);
  border-radius: 9px;
  border: 1.5px solid var(--border-color);
  padding: 0.38rem 0.55rem;
  box-shadow: var(--shadow);
  cursor: pointer;
  pointer-events: auto;
  transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease, opacity 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}}
.person-card:hover {{
  transform: translateY(-2px) scale(1.02);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent);
  z-index: 50;
}}
.person-card.sex-M {{ border-left: 4.5px solid var(--male-border); }}
.person-card.sex-F {{ border-left: 4.5px solid var(--female-border); }}

.person-card.is-proband {{
  border: 2px solid #f59e0b;
  border-left: 6px solid #f59e0b;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(239, 68, 68, 0.08));
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.35);
}}

.card-anchor {{
  position: absolute;
  top: calc(50% - 4px);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--border-color);
  border: 1.5px solid var(--bg-card);
  pointer-events: none;
}}
.card-anchor.left {{ left: -4px; }}
.card-anchor.right {{ right: -4px; }}
.person-card:hover .card-anchor {{ background: var(--accent); }}

.person-card.highlighted {{
  border-color: #f59e0b !important;
  box-shadow: 0 0 16px rgba(245, 158, 11, 0.7) !important;
  transform: translateY(-2px) scale(1.03);
  z-index: 45;
}}
#cardsLayer .person-card.dimmed {{
  opacity: 0.22;
}}
#generationsContainer .person-card {{
  opacity: 1 !important;
}}

.card-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.68rem;
  line-height: 1;
  white-space: nowrap;
  gap: 0.25rem;
}}
.card-gen {{
  font-weight: 700;
  color: var(--text-muted);
  background: var(--bg-primary);
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.card-sex {{ font-size: 0.8rem; }}
.badge-veteran {{
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  background: linear-gradient(135deg, #dc2626, #991b1b);
  color: #ffffff;
  font-size: 0.62rem;
  font-weight: 700;
  padding: 0.08rem 0.35rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(185, 28, 28, 0.3);
  letter-spacing: 0.02em;
}}
.badge-doc-tree {{
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  background: rgba(37, 99, 235, 0.14);
  color: #2563eb;
  border: 1px solid rgba(37, 99, 235, 0.35);
  font-size: 0.62rem;
  font-weight: 700;
  padding: 0.08rem 0.35rem;
  border-radius: 4px;
  cursor: pointer;
  letter-spacing: 0.02em;
  transition: all 0.15s ease;
}}
.badge-reconstructed {{
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  background: linear-gradient(135deg, #d97706, #b45309);
  color: #ffffff;
  font-size: 0.58rem;
  font-weight: 700;
  padding: 0.08rem 0.35rem;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(180, 83, 9, 0.25);
  letter-spacing: 0.02em;
}}
.person-card.is-reconstructed {{
  border: 2px dashed #d97706 !important;
  background: linear-gradient(135deg, rgba(254, 252, 191, 0.45), rgba(255, 255, 255, 0.96)) !important;
}}
.badge-doc-tree:hover {{
  background: #2563eb;
  color: #ffffff;
  transform: scale(1.05);
}}
[data-theme="dark"] .badge-doc-tree {{
  background: rgba(59, 130, 246, 0.22);
  color: #93c5fd;
  border-color: rgba(59, 130, 246, 0.45);
}}
[data-theme="dark"] .badge-doc-tree:hover {{
  background: #2563eb;
  color: #ffffff;
}}
.person-card.has-archival-docs {{
  border-bottom: 2.5px solid #2563eb;
}}
.card-name {{
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.15;
}}
.card-meta {{
  font-size: 0.70rem;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
  align-items: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.1;
}}
.card-dates {{ font-weight: 500; }}
.card-place {{
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 105px;
}}
.card-tag {{
  display: inline-block;
  font-size: 0.64rem;
  font-weight: 600;
  padding: 0.08rem 0.35rem;
  border-radius: 3px;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

/* FLOATING ZOOM TOOLS */
.tree-floating-tools {{
  position: absolute;
  bottom: 1.25rem;
  right: 1.25rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 0.35rem;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  z-index: 60;
}}
.tree-floating-tools button {{
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--bg-surface);
  color: var(--text-main);
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}}
.tree-floating-tools button:hover {{
  background: var(--accent-light);
  color: var(--accent);
  border-color: var(--accent);
}}

/* LEGEND */
.tree-legend {{
  position: absolute;
  bottom: 1.25rem;
  left: 1.25rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 0.6rem 0.8rem;
  box-shadow: var(--shadow-lg);
  font-size: 0.72rem;
  z-index: 60;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}}
.legend-item {{ display: flex; align-items: center; gap: 0.45rem; }}
.legend-line {{
  width: 18px;
  height: 3px;
  border-radius: 2px;
}}

/* OTHER VIEWS */

#view-list, #view-table, #view-archive, #view-info, #view-sources, #view-stats {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  overflow-y: auto;
  height: 100%;
  box-sizing: border-box;
}}

.gen-section {{ margin-bottom: 2rem; }}
.gen-title {{
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.85rem;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.cards-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 0.85rem;
}}

/* VETERAN CARDS */
.veteran-cards-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.25rem;
}}
.veteran-card {{
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  flex-wrap: nowrap !important;
  box-sizing: border-box !important;
  width: 100% !important;
}}
.veteran-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.6rem;
  gap: 0.5rem;
}}

.table-container {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}}
table {{
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.85rem;
}}
th {{
  background: var(--bg-primary);
  padding: 0.65rem 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-color);
}}
td {{
  padding: 0.65rem 0.85rem;
  border-bottom: 1px solid var(--border-color);
}}
tr:hover td {{
  background: var(--accent-light);
  cursor: pointer;
}}

.info-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1.25rem;
  margin-bottom: 1.25rem;
  box-shadow: var(--shadow);
}}
.info-card h2 {{
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.65rem;
  color: var(--accent);
}}
.info-card p {{
  font-size: 0.9rem;
  line-height: 1.55;
  margin-bottom: 0.65rem;
}}
.info-card ul {{
  padding-left: 1.25rem;
  line-height: 1.55;
  font-size: 0.9rem;
}}

.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}}
.stat-box {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1rem;
  text-align: center;
  box-shadow: var(--shadow);
}}
.stat-number {{
  font-size: 2rem;
  font-weight: 800;
  color: var(--accent);
  line-height: 1.1;
}}
.stat-label {{
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
  font-weight: 600;
}}


.flow-reverse .tree-link {{
  animation: flowLineRev 1.5s linear infinite !important;
}}
@keyframes flowLineRev {{
  to {{ stroke-dashoffset: 28; }}
}}



/* MODAL */
.modal-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  box-sizing: border-box;
}}
.modal-overlay.open {{ display: flex; }}
.modal-card {{
  width: 92%;
  max-width: 580px;
  max-height: calc(100vh - 2rem);
  max-height: calc(100dvh - 2rem);
  background: var(--bg-surface);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  margin: auto;
  animation: modalIn 0.18s ease-out;
}}
@keyframes modalIn {{
  from {{ opacity: 0; transform: scale(0.95); }}
  to {{ opacity: 1; transform: scale(1); }}
}}

.modal-header {{
  padding: 1.1rem 1.35rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}}
.modal-title h2 {{
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1.25;
}}
.modal-close {{
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted);
  cursor: pointer;
  line-height: 1;
}}
.modal-body {{
  padding: 1.25rem 1.35rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}
.detail-group h3 {{
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  margin-bottom: 0.35rem;
}}
.detail-item {{
  font-size: 0.88rem;
  color: var(--text-main);
  line-height: 1.4;
}}
.link-badge {{
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-main);
  cursor: pointer;
  margin-right: 0.35rem;
  margin-bottom: 0.35rem;
  text-decoration: none;
  transition: all 0.15s ease;
}}
.link-badge:hover {{
  border-color: var(--accent);
  background: var(--accent-light);
  color: var(--accent);
}}

button, .person-card, .pill-btn, .subbar-btn, .nav-tab, .modal-close {{
  touch-action: manipulation;
}}

.header-top {{
  display: contents;
}}


/* ARCHIVE TAB & DOC VIEWER STYLES */
.archive-header-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.25rem;
}}
.archive-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1.15rem;
}}
.doc-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}}
.doc-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(0,0,0,0.12);
  border-color: var(--accent);
}}
.doc-card-thumb-wrap {{
  position: relative;
  width: 100%;
  height: 190px;
  background: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}}
.doc-card-thumb-wrap img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  transition: transform 0.3s ease;
}}
.doc-card:hover .doc-card-thumb-wrap img {{
  transform: scale(1.05);
}}
.doc-badge-overlay {{
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(4px);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.22rem 0.55rem;
  border-radius: 5px;
  border: 1px solid rgba(255,255,255,0.2);
}}
.doc-zoom-hint {{
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(4px);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.22rem 0.55rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}}
.doc-card-content {{
  padding: 0.95rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: space-between;
}}
.doc-card-title {{
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
  margin-bottom: 0.35rem;
}}
.doc-card-meta {{
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  line-height: 1.4;
}}
.doc-card-desc {{
  font-size: 0.8rem;
  color: var(--text-main);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.75rem;
}}
.doc-card-actions {{
  display: flex;
  gap: 0.45rem;
  border-top: 1px solid var(--border-color);
  padding-top: 0.65rem;
  margin-top: auto;
}}

/* LIGHTBOX DOC VIEWER */
.doc-viewer-modal {{
  position: fixed;
  inset: 0;
  background: rgba(10, 15, 29, 0.92);
  backdrop-filter: blur(8px);
  z-index: 99999;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  box-sizing: border-box;
  overflow: hidden;
}}
.doc-viewer-modal.open {{
  display: flex;
}}
.doc-viewer-container {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  height: auto;
  max-height: calc(100vh - 2.5rem);
  max-height: calc(100dvh - 2.5rem);
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 60px rgba(0,0,0,0.6);
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  position: relative;
  box-sizing: border-box;
  margin: auto;
}}
.doc-viewer-header {{
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-primary);
  gap: 0.75rem;
  position: sticky;
  top: 0;
  z-index: 30;
  flex-shrink: 0;
}}
.doc-viewer-badge {{
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  border: 1px solid transparent;
}}
.doc-viewer-actions {{
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}}
.doc-close-btn {{
  background: rgba(239, 68, 68, 0.1);
  border: 1.5px solid rgba(239, 68, 68, 0.35);
  color: #ef4444;
  padding: 0.4rem 0.85rem;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.15s ease;
  white-space: nowrap;
  flex-shrink: 0;
}}
.doc-close-btn:hover {{
  background: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);
}}
.doc-img-hint-badge {{
  position: absolute;
  bottom: 0.65rem;
  right: 0.65rem;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(4px);
  color: #f1f5f9;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.3rem 0.65rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  pointer-events: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
}}
.doc-viewer-viewport {{
  flex: 1 0 auto;
  min-height: 48vh;
  position: relative;
  background: #080d1a;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem;
  box-sizing: border-box;
}}
.doc-nav-btn {{
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(30, 41, 59, 0.85);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.25);
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}}
.doc-nav-btn:hover {{
  background: var(--accent);
  transform: translateY(-50%) scale(1.1);
  border-color: var(--accent);
}}
.doc-nav-btn.prev {{ left: 1rem; }}
.doc-nav-btn.next {{ right: 1rem; }}
.doc-img-wrapper {{
  width: 100%;
  max-width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}}
#docViewerImg {{
  max-width: 100%;
  height: auto;
  max-height: 72vh;
  object-fit: contain;
  box-shadow: 0 6px 30px rgba(0,0,0,0.7);
  border-radius: 4px;
}}
.doc-viewer-footer {{
  padding: 0.75rem 1.25rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-primary);
  gap: 1rem;
  flex-shrink: 0;
}}
.doc-viewer-footer-counter {{
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-muted);
  white-space: nowrap;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
}}

/* MINI THUMBNAILS GRID FOR PERSON MODALS & HERO CARDS */
.person-docs-mini-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(105px, 1fr));
  gap: 0.55rem;
  margin-top: 0.45rem;
}}
.person-doc-thumb-item {{
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--border-color);
  background: #0f172a;
  aspect-ratio: 4/3;
  position: relative;
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease;
}}
.person-doc-thumb-item:hover {{
  transform: scale(1.05);
  border-color: var(--accent);
  z-index: 2;
}}
.person-doc-thumb-item img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
}}
.person-doc-thumb-item .thumb-label {{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(2px);
  color: #fff;
  font-size: 0.64rem;
  padding: 0.15rem 0.25rem;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600;
}}

/* FULLSCREEN SCAN LIGHTBOX MODAL WITH ZOOM & PAN */
.fs-scan-modal {{
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  background: rgba(4, 7, 16, 0.96);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 100000;
  display: none;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  animation: fsIn 0.2s ease-out;
}}
@keyframes fsIn {{
  from {{ opacity: 0; transform: scale(0.98); }}
  to {{ opacity: 1; transform: scale(1); }}
}}
.fs-scan-modal.open {{
  display: flex;
}}

.fs-scan-header {{
  height: 52px;
  min-height: 52px;
  padding: 0 1rem;
  background: rgba(11, 15, 25, 0.92);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  z-index: 10;
  flex-shrink: 0;
  box-sizing: border-box;
}}
.fs-scan-info {{
  display: flex;
  flex-direction: column;
  min-width: 0;
}}
.fs-scan-title {{
  font-size: 0.92rem;
  font-weight: 700;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.fs-scan-meta {{
  font-size: 0.72rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

.fs-scan-tools {{
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}}
.fs-tool-btn {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: 6px;
  padding: 0.32rem 0.6rem;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}}
.fs-tool-btn:hover {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.fs-close-btn {{
  background: #dc2626;
  border: 1px solid #b91c1c;
  color: #fff;
  border-radius: 6px;
  padding: 0.35rem 0.8rem;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}}
.fs-close-btn:hover {{
  background: #ef4444;
}}

.fs-scan-viewport {{
  flex: 1 1 0;
  min-height: 0;
  width: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  user-select: none;
  touch-action: none;
  background: #03060f;
  box-sizing: border-box;
}}
.fs-scan-viewport:active, .fs-scan-viewport.dragging {{
  cursor: grabbing;
}}

.fs-scan-img-container {{
  position: absolute;
  transform-origin: center center;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.05s linear;
  will-change: transform;
}}
#fsScanImg {{
  max-width: 95vw;
  max-height: 86vh;
  object-fit: contain;
  box-shadow: 0 10px 40px rgba(0,0,0,0.85);
  border-radius: 4px;
  pointer-events: none;
}}

/* FLOATING ZOOM CONTROLS AT BOTTOM FOR MOBILE & DESKTOP */
.fs-floating-tools {{
  position: absolute;
  bottom: 1.25rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.45rem;
  background: rgba(17, 24, 39, 0.9);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.55rem;
  border-radius: 30px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 20;
}}
.fs-float-btn {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  border-radius: 20px;
  padding: 0.32rem 0.7rem;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}}
.fs-float-btn:hover {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.fs-float-close {{
  background: #dc2626;
  border-color: #b91c1c;
  color: #fff;
  font-weight: 700;
}}
.fs-float-close:hover {{
  background: #ef4444;
}}

@media (max-width: 600px) {{
  .fs-scan-tools .fs-tool-btn {{
    display: none;
  }}
  .fs-floating-tools {{
    bottom: 0.85rem;
    padding: 0.3rem 0.45rem;
    gap: 0.35rem;
  }}
  .fs-float-btn {{
    padding: 0.28rem 0.55rem;
    font-size: 0.72rem;
  }}
}}

.card-gen {{
  cursor: pointer;
  transition: color 0.15s ease;
}}
.card-gen:hover {{
  color: var(--accent) !important;
  text-decoration: underline;
}}
.person-card.is-hidden-branch {{
  display: none !important;
}}
.tree-link.is-hidden-branch {{
  display: none !important;
}}

.gen-select-dropdown {{
  padding: 0.22rem 0.45rem;
  border-radius: 5px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-main);
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  max-width: 145px;
  transition: border-color 0.15s ease;
}}
.gen-select-dropdown:hover, .gen-select-dropdown:focus {{
  border-color: var(--accent);
}}

.branch-select-dropdown {{
  display: none;
}}
.branch-pill-buttons {{
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}}

/* MOBILE MENU DRAWER & BUTTON */
.mobile-menu-btn {{
  display: none;
  align-items: center;
  gap: 0.35rem;
  background: var(--bg-primary);
  color: var(--text-main);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.35rem 0.65rem;
  font-size: 0.84rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  flex-shrink: 0;
}}
.mobile-menu-btn:hover, .mobile-menu-btn:active {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}

.mobile-drawer-backdrop {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 2999;
  display: none;
  opacity: 0;
  transition: opacity 0.25s ease;
}}
.mobile-drawer-backdrop.open {{
  display: block;
  opacity: 1;
}}

.mobile-drawer {{
  position: fixed;
  top: 0;
  right: -340px;
  width: min(320px, 86vw);
  height: 100vh;
  height: 100dvh;
  background: var(--bg-surface);
  border-left: 1px solid var(--border-color);
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
  z-index: 3000;
  display: flex;
  flex-direction: column;
  transition: right 0.26s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
}}
.mobile-drawer.open {{
  right: 0;
}}
.mobile-drawer-header {{
  padding: 0.85rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-primary);
  flex-shrink: 0;
}}
.mobile-drawer-brand {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.mobile-drawer-close {{
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.05rem;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s ease;
}}
.mobile-drawer-close:hover {{
  color: var(--text-main);
  border-color: var(--accent);
}}
.mobile-drawer-body {{
  padding: 0.9rem;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}}
.drawer-search-container {{
  position: relative;
  width: 100%;
}}
.drawer-search-container .search-box {{
  width: 100%;
}}
.drawer-search-container .search-box input {{
  width: 100% !important;
  box-sizing: border-box !important;
}}
.drawer-search-results {{
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  max-height: 220px;
  overflow-y: auto;
  z-index: 100;
  display: none;
  margin-top: 4px;
}}
.drawer-search-results.open {{
  display: block;
}}
.drawer-theme-box {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.3rem 0.2rem;
}}
.drawer-divider {{
  height: 1px;
  background: var(--border-color);
  margin: 0.2rem 0;
}}
.drawer-nav-title {{
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.2rem;
}}
.drawer-nav-list {{
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}}
.drawer-nav-item {{
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  border: 1px solid transparent;
  background: var(--bg-primary);
  color: var(--text-main);
  font-size: 0.88rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
  box-sizing: border-box;
}}
.drawer-nav-item:hover, .drawer-nav-item.active {{
  background: var(--accent-light);
  border-color: var(--accent);
  color: var(--accent);
}}
.drawer-nav-icon {{
  font-size: 1.15rem;
  line-height: 1;
}}
.drawer-nav-badge {{
  margin-left: auto;
  font-size: 0.72rem;
  padding: 0.12rem 0.45rem;
  border-radius: 10px;
  background: rgba(37, 99, 235, 0.15);
  color: var(--accent);
  font-weight: 700;
}}
.mobile-drawer-footer {{
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-primary);
  flex-shrink: 0;
}}

/* BOTTOM ANCHOR NAVIGATION BAR */
.info-bottom-bar {{
  position: sticky;
  bottom: 0.65rem;
  left: 0;
  right: 0;
  width: 100%;
  max-width: 640px;
  margin: 1.5rem auto 0.35rem auto;
  z-index: 80;
  pointer-events: auto;
  box-sizing: border-box;
  padding: 0 0.25rem;
}}
.info-bottom-scroll {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.3rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 30px;
  padding: 0.28rem 0.35rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}}
.info-bottom-pill {{
  flex: 1 1 0;
  min-width: 0;
  padding: 0.35rem 0.35rem;
  border-radius: 20px;
  background: var(--bg-primary);
  color: var(--text-main);
  text-decoration: none;
  font-size: 0.74rem;
  font-weight: 600;
  border: 1px solid var(--border-color);
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  white-space: nowrap;
  box-sizing: border-box;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.info-bottom-pill:hover, .info-bottom-pill.active {{
  background: var(--accent);
  color: #fff !important;
  border-color: var(--accent);
  box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}}

.pill-lbl-short {{ display: none; }}
.pill-lbl-full {{ display: inline; }}

@media (max-width: 680px) {{
  .info-bottom-bar {{
    bottom: 0.45rem !important;
    padding: 0 0.15rem !important;
    margin: 1rem auto 0.2rem auto !important;
    max-width: 100% !important;
  }}
  .info-bottom-scroll {{
    padding: 0.22rem 0.25rem !important;
    gap: 0.2rem !important;
    border-radius: 24px !important;
  }}
  .info-bottom-pill {{
    padding: 0.3rem 0.15rem !important;
    font-size: 0.69rem !important;
    gap: 0.15rem !important;
    border-radius: 16px !important;
  }}
  .pill-lbl-short {{ display: inline !important; }}
  .pill-lbl-full {{ display: none !important; }}
}}

@media (max-width: 380px) {{
  .info-bottom-pill {{
    font-size: 0.64rem !important;
    padding: 0.26rem 0.1rem !important;
  }}
}}

@media (max-width: 820px) {{
  header {{
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0 0.75rem !important;
    gap: 0.5rem !important;
  }}
  .header-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }}
  .brand-text h1 {{ font-size: 0.95rem; margin: 0; padding: 0; line-height: 1.15; }}
  .brand-badge {{ display: block; font-size: 0.64rem; line-height: 1.1; margin-top: 1px; }}
  .header-right {{
    display: none !important;
  }}
  .nav-tabs {{
    display: none !important;
  }}
  .mobile-menu-btn {{
    display: inline-flex !important;
  }}
  #view-info, #view-sources {{
    padding-bottom: 4.8rem !important;
  }}
  .tree-subbar {{
    top: 0.35rem;
    left: 0.45rem;
    right: 0.45rem;
    flex-direction: column;
    align-items: stretch;
    gap: 0.35rem;
    pointer-events: none;
  }}
  .tree-subbar-left {{
    display: flex !important;
    align-items: center !important;
    gap: 0.35rem !important;
    overflow-x: auto;
    white-space: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    padding: 0.25rem 0.4rem;
    width: 100%;
    box-sizing: border-box;
    pointer-events: auto;
  }}
  .tree-subbar-left::-webkit-scrollbar {{ display: none; }}
  .branch-select-dropdown {{
    display: inline-block !important;
    max-width: 105px !important;
  }}
  .branch-pill-buttons {{
    display: none !important;
  }}
  .gen-select-dropdown {{
    max-width: 105px !important;
  }}
  .tree-subbar-right {{ display: none; }}
  .pinned-gen-bar {{ top: 46px; }}
  .tree-legend {{ display: none; }}
  .tree-floating-tools {{
    bottom: 1rem;
    right: 0.75rem;
    padding: 0.3rem;
    gap: 0.35rem;
  }}
  .tree-floating-tools button {{
    width: 44px;
    height: 44px;
    font-size: 1.15rem;
    border-radius: 8px;
  }}
  .modal-card {{
    width: 95% !important;
    max-width: 95% !important;
    max-height: calc(100vh - 1.5rem) !important;
    max-height: calc(100dvh - 1.5rem) !important;
    border-radius: 12px;
  }}
  .modal-header {{
    padding: 0.85rem 1rem;
  }}
  .modal-body {{
    padding: 0.85rem 1rem;
  }}
  
  .doc-viewer-modal {{
    padding: 0.6rem !important;
    padding-top: max(0.6rem, env(safe-area-inset-top)) !important;
    padding-bottom: max(0.6rem, env(safe-area-inset-bottom)) !important;
    padding-left: max(0.6rem, env(safe-area-inset-left)) !important;
    padding-right: max(0.6rem, env(safe-area-inset-right)) !important;
    box-sizing: border-box !important;
  }}
  .doc-viewer-container {{
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: calc(100vh - 1.2rem) !important;
    max-height: calc(100dvh - 1.2rem) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border-color) !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
    margin: auto 0 !important;
  }}
  .doc-nav-btn {{ width: 38px; height: 38px; font-size: 1.1rem; }}
  .doc-nav-btn.prev {{ left: 0.4rem; }}
  .doc-nav-btn.next {{ right: 0.4rem; }}
  .doc-viewer-header {{
    padding: 0.55rem 0.75rem !important;
    gap: 0.5rem !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 30 !important;
  }}
  .doc-close-btn {{ padding: 0.35rem 0.65rem !important; font-size: 0.78rem !important; }}
  .doc-viewer-viewport {{
    min-height: 280px !important;
    padding: 0.5rem !important;
  }}
  #docViewerImg {{
    max-height: 55vh !important;
  }}
  .doc-viewer-footer {{ padding: 0.55rem 0.75rem; flex-direction: column; align-items: flex-start; gap: 0.4rem; }}
  .doc-viewer-footer-counter {{ align-self: flex-end; }}

  /* COMPACT MOBILE VIEWS & CONTAINMENT */
  #view-list, #view-table, #view-archive, #view-info, #view-sources, #view-stats {{
    padding: 0.75rem 0.5rem !important;
    overflow-x: hidden !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }}

  /* INFO CARDS: Prevent horizontal overflow */
  .info-card, .archive-header-card {{
    padding: 0.85rem 0.75rem !important;
    margin-bottom: 0.75rem !important;
    border-radius: 8px !important;
    box-sizing: border-box !important;
    width: 100% !important;
    overflow: hidden !important;
  }}
  .info-card h2 {{
    font-size: 1.08rem !important;
    line-height: 1.3 !important;
  }}
  .info-card h3 {{
    font-size: 0.95rem !important;
    line-height: 1.35 !important;
  }}
  .info-card p, .info-card li {{
    font-size: 0.84rem !important;
    line-height: 1.5 !important;
  }}
  .info-card ul {{
    padding-left: 1.15rem !important;
  }}

  /* FORCE ALL MULTI-COLUMN GRIDS TO SINGLE COLUMN ON MOBILE (Zero overflow) */
  .archive-grid,
  .cards-grid,
  div[style*="grid-template-columns:repeat(auto-fit"],
  div[style*="grid-template-columns: repeat(auto-fit"],
  div[style*="grid-template-columns:repeat(auto-fill"],
  div[style*="grid-template-columns: repeat(auto-fill"] {{
    grid-template-columns: 1fr !important;
    gap: 0.75rem !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }}

  /* STATS BANNER: 2 neat columns */
  .stats-grid,
  div[style*="minmax(180px, 1fr)"],
  div[style*="minmax(210px, 1fr)"] {{
    grid-template-columns: 1fr 1fr !important;
    gap: 0.5rem !important;
  }}
  .stat-card {{
    padding: 0.65rem 0.45rem !important;
  }}
  .stat-number {{ font-size: 1.45rem !important; }}
  .stat-label {{ font-size: 0.74rem !important; }}

  /* FLEX CONTAINERS INSIDE CARDS: Auto-wrap to prevent bursting */
  .info-card div[style*="display:flex"]:not(.veteran-card),
  .archive-header-card div[style*="display:flex"] {{
    flex-wrap: wrap !important;
    gap: 0.4rem !important;
    max-width: 100% !important;
  }}

  /* VETERAN CARDS MOBILE ADAPTATION */
  .veteran-cards-grid {{
    grid-template-columns: 1fr !important;
    gap: 0.75rem !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }}
  .veteran-card {{
    padding: 0.85rem 0.75rem !important;
    display: flex !important;
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
    box-sizing: border-box !important;
    width: 100% !important;
  }}
  .veteran-card-header {{
    flex-wrap: wrap !important;
    gap: 0.35rem !important;
  }}
  .veteran-card .pill-btn {{
    white-space: normal !important;
    word-break: break-word !important;
    text-align: left !important;
    line-height: 1.35 !important;
  }}

  /* CHURCH & BOOK PHOTOS ON MOBILE: Full-width banner style */
  div[style*="gap:0.85rem"][style*="margin-bottom:0.75rem"],
  div[style*="gap:1rem"][style*="margin-bottom:1rem"] {{
    flex-direction: column !important;
    align-items: stretch !important;
  }}
  div[style*="gap:0.85rem"] img,
  div[style*="gap:1rem"] img {{
    width: 100% !important;
    max-width: 100% !important;
    height: 165px !important;
    max-height: 180px !important;
    object-fit: cover !important;
    margin-bottom: 0.35rem !important;
    border-radius: 6px !important;
  }}

  /* ARCHIVE TOOLBAR & SEARCH ON MOBILE */
  .archive-toolbar {{
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 0.6rem !important;
  }}
  .archive-search-box {{
    width: 100% !important;
    min-width: 0 !important;
  }}
  .archive-filter-pills {{
    width: 100% !important;
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch !important;
    padding-bottom: 0.35rem !important;
    scrollbar-width: none;
  }}
  .archive-filter-pills::-webkit-scrollbar {{ display: none; }}
  .archive-filter-pills .pill-btn {{
    flex-shrink: 0 !important;
  }}

  /* TABLE VIEW: Smooth contained scroll without page blowout */
  .table-container {{
    width: 100% !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    border-radius: 8px !important;
  }}
  table {{
    min-width: 580px !important;
    font-size: 0.8rem !important;
  }}
  th, td {{
    padding: 0.45rem 0.5rem !important;
  }}

  /* PERSON MODAL THUMBNAILS ON MOBILE */
  .person-docs-mini-grid {{
    grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)) !important;
    gap: 0.4rem !important;
  }}
  .thumb-label {{
    font-size: 0.6rem !important;
    padding: 0.1rem 0.2rem !important;
  }}

  /* PILL BUTTONS & LINKS: Accessible tap targets */
  .pill-btn {{
    padding: 0.28rem 0.55rem !important;
    font-size: 0.74rem !important;
  }}
  .link-badge {{
    padding: 0.35rem 0.65rem !important;
    font-size: 0.78rem !important;
    display: inline-block !important;
    margin: 0.15rem 0 !important;
    max-width: 100% !important;
    white-space: normal !important;
    word-break: break-word !important;
  }}

  /* WORD BREAK & TEXT OVERFLOW SAFETY */
  .info-card div, .info-card p, .info-card li, .modal-body div {{
    word-break: break-word;
    overflow-wrap: break-word;
  }}
}}

@media (max-width: 480px) {{
  header {{
    padding: 0 0.55rem !important;
  }}
  .brand-text h1 {{ font-size: 0.88rem !important; }}
  .brand-badge {{ display: none !important; }}
  .mobile-menu-btn {{ padding: 0.3rem 0.55rem !important; font-size: 0.8rem !important; }}
  .info-card {{ padding: 0.75rem 0.6rem !important; }}
  .stat-number {{ font-size: 1.35rem !important; }}
}}
</style>
</head>
<body>

<!-- RESPONSIVE HEADER -->
<header>
  <div class="header-top">
    <div class="brand">
      <span class="brand-icon">🌳</span>
      <div class="brand-text">
        <h1>Родословная Туркиных</h1>
        <span class="brand-badge">{max_gen} поколений • {total_persons} персон</span>
      </div>
    </div>

    <div class="header-right">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="Поиск персоны..." oninput="handleSearch(this.value)">
      </div>
      <button class="btn-icon" onclick="toggleTheme()" title="Сменить тему оформления">🌓</button>
    </div>

    <button class="mobile-menu-btn" onclick="openMobileMenu()" aria-label="Открыть меню">
      <span>☰</span> <span>Меню</span>
    </button>
  </div>

  <nav class="nav-tabs">
    <button class="nav-tab active" onclick="switchTab('tree')">🌿 Древо</button>
    <button class="nav-tab" onclick="switchTab('list')">📜 Поколения</button>
    <button class="nav-tab" onclick="switchTab('table')">📋 Таблица</button>
    <button class="nav-tab" onclick="switchTab('archive')">🏛️ Архив документов <span style="font-size:0.75rem; background:rgba(37,99,235,0.15); padding:0.1rem 0.4rem; border-radius:10px; margin-left:3px;">{len(archive_catalog.DOCS_CATALOG)}</span></button>
    <button class="nav-tab" onclick="switchTab('info')">🗺️ Места и роды</button>
    <button class="nav-tab" onclick="switchTab('sources')">📚 Источники</button>
    <button class="nav-tab" onclick="switchTab('stats')">📊 Статистика</button>
  </nav>
</header>

<!-- MOBILE DRAWER MENU & BACKDROP -->
<div id="mobileDrawerBackdrop" class="mobile-drawer-backdrop" onclick="closeMobileMenu()"></div>
<aside id="mobileDrawer" class="mobile-drawer" aria-label="Мобильное меню навигации">
  <div class="mobile-drawer-header">
    <div class="mobile-drawer-brand">
      <span style="font-size:1.35rem;">🌳</span>
      <div style="font-weight:700; font-size:0.92rem; line-height:1.2;">Родословная Туркиных</div>
    </div>
    <button class="mobile-drawer-close" onclick="closeMobileMenu()" title="Закрыть меню">✕</button>
  </div>

  <div class="mobile-drawer-body">
    <!-- SEARCH IN DRAWER -->
    <div class="drawer-search-container">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="drawerSearchInput" placeholder="Поиск персоны..." oninput="handleDrawerSearch(this.value)">
      </div>
      <div id="drawerSearchResults" class="drawer-search-results"></div>
    </div>

    <!-- THEME TOGGLE -->
    <div class="drawer-theme-box">
      <span style="font-size:0.82rem; font-weight:600; color:var(--text-muted);">Тема оформления:</span>
      <button class="pill-btn" onclick="toggleTheme()" id="drawerThemeBtn" style="font-size:0.78rem; padding:0.3rem 0.7rem;">
        <span id="drawerThemeIcon">🌓</span> <span id="drawerThemeText">Тема</span>
      </button>
    </div>

    <div class="drawer-divider"></div>

    <!-- VERTICAL NAVIGATION ITEMS -->
    <div class="drawer-nav-title">Разделы:</div>
    <nav class="drawer-nav-list">
      <button class="drawer-nav-item active" data-tab="tree" onclick="handleDrawerNav('tree')">
        <span class="drawer-nav-icon">🌿</span>
        <span>Интерактивное древо</span>
      </button>
      <button class="drawer-nav-item" data-tab="list" onclick="handleDrawerNav('list')">
        <span class="drawer-nav-icon">📜</span>
        <span>Поколения (роспись)</span>
      </button>
      <button class="drawer-nav-item" data-tab="table" onclick="handleDrawerNav('table')">
        <span class="drawer-nav-icon">📋</span>
        <span>Таблица всех персон</span>
      </button>
      <button class="drawer-nav-item" data-tab="archive" onclick="handleDrawerNav('archive')">
        <span class="drawer-nav-icon">🏛️</span>
        <span>Архив документов</span>
        <span class="drawer-nav-badge">{len(archive_catalog.DOCS_CATALOG)}</span>
      </button>
      <button class="drawer-nav-item" data-tab="info" onclick="handleDrawerNav('info')">
        <span class="drawer-nav-icon">🗺️</span>
        <span>Места и роды</span>
      </button>
      <button class="drawer-nav-item" data-tab="sources" onclick="handleDrawerNav('sources')">
        <span class="drawer-nav-icon">📚</span>
        <span>Источники и литература</span>
      </button>
      <button class="drawer-nav-item" data-tab="stats" onclick="handleDrawerNav('stats')">
        <span class="drawer-nav-icon">📊</span>
        <span>Статистика древа</span>
      </button>
    </nav>
  </div>

  <div class="mobile-drawer-footer">
    <div style="font-size:0.72rem; color:var(--text-muted); text-align:center;">
      {max_gen} поколений • {total_persons} персон • 1490–2024 гг.
    </div>
  </div>
</aside>

<main>
  <!-- TAB 1: VISUAL TREE VIEW WITH SVG CONNECTORS & ARROWS -->
  <div id="view-tree" class="view-section active">
    <!-- SUB-TOOLBAR FOR TREE VIEW -->
    <div class="tree-subbar">
      <div class="tree-subbar-left">
        <button class="pill-btn" id="btnToggleDirectLine" onclick="toggleDirectLine()" title="Показать только прямую линию предков Николая">🎯 Прямая линия</button>
        <select class="gen-select-dropdown" id="genSelectDropdown" onchange="if(this.value) focusGeneration(parseInt(this.value));" title="Перейти к поколению">
          <option value="">Поколения ▾</option>
          <option value="1">I: Николай (2024)</option>
          <option value="2">II: Родители (1991)</option>
          <option value="3">III: Дедушки (1961–1970)</option>
          <option value="4">IV: Прадедушки (1906–1935)</option>
          <option value="5">V: Михаил Туркин (1906)</option>
          <option value="6">VI: Николай Алексеевич (1876)</option>
          <option value="7">VII: Алексей Иванович (1852)</option>
          <option value="8">VIII: Иван Алексеевич (1825)</option>
          <option value="9">IX: Алексей Григорьевич (1778)</option>
          <option value="10">X: Григорий Степанович (1751)</option>
          <option value="11">XI: Степан Иванович (1720)</option>
          <option value="12">XII: Иван Петрович (1710)</option>
          <option value="13">XIII: Священник Пётр (1678)</option>
          <option value="14">XIV: Дьячок Исаак (1678)</option>
          <option value="15">XV: Приказной Афанасий (1646)</option>
          <option value="16">XVI: Патриарх Семён (~1608)</option>
          <option value="20">XX: Турка малой (1490)</option>
        </select>
        <select class="gen-select-dropdown branch-select-dropdown" id="branchSelectDropdown" onchange="if(this.value) focusPerson(this.value);" title="Перейти к ветви рода">
          <option value="">Ветви ▾</option>
          <option value="I2">🏛️ Туркины</option>
          <option value="I14">🌾 Шехонины</option>
          <option value="I10">🌲 Шуктомовы</option>
          <option value="I16">📜 Зиновьевы</option>
          <option value="I3">🌴 Таиланд</option>
        </select>
        <div class="branch-pill-buttons">
          <span class="subbar-label" style="margin-left:0.25rem;">Ветви:</span>
          <button class="pill-btn" onclick="focusPerson('I2')">🏛️ Туркины</button>
          <button class="pill-btn" onclick="focusPerson('I14')">🌾 Шехонины</button>
          <button class="pill-btn" onclick="focusPerson('I10')">🌲 Шуктомовы</button>
          <button class="pill-btn" onclick="focusPerson('I16')">📜 Зиновьевы</button>
          <button class="pill-btn" onclick="focusPerson('I3')">🌴 Таиланд</button>
        </div>
      </div>

      <div class="tree-subbar-right">
        <button class="subbar-btn active" id="btnToggleSpouses" onclick="toggleSpouseLinks()" title="Показать или скрыть брачные союзы">💍 Браки</button>
      </div>
    </div>

    <!-- PINNED GENERATION BAR AT TOP OF TREE -->
    <div class="pinned-gen-bar">
      <div class="pinned-gen-track" id="pinnedGenTrack"></div>
    </div>

    <!-- CANVAS WITH SVG AND CARDS -->
    <div class="tree-canvas" id="treeCanvas">
      <svg id="treeSvg" viewBox="0 0 {canvas_w} {canvas_h}">
        <defs>
          <!-- Arrow Markers End (Child -> Parent) -->
          <marker id="arrow-father" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 7 5 L 1 8 z" fill="#2563eb" />
          </marker>
          <marker id="arrow-mother" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 7 5 L 1 8 z" fill="#db2777" />
          </marker>
          <marker id="arrow-highlight" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#f59e0b" />
          </marker>
          <marker id="arrow-research" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 7 5 L 1 8 z" fill="#a855f7" />
          </marker>

          <!-- Arrow Markers Start (Parent -> Child) -->
          <marker id="arrow-start-father" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 8 1.5 L 0 5 L 8 8.5 z" fill="#2563eb" />
          </marker>
          <marker id="arrow-start-mother" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 8 1.5 L 0 5 L 8 8.5 z" fill="#db2777" />
          </marker>
          <marker id="arrow-start-highlight" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M 8 1.5 L 0 5 L 8 8.5 z" fill="#f59e0b" />
          </marker>
        </defs>

        <g id="svgSpouseLayer"></g>
        <g id="svgLinksLayer"></g>
      </svg>

      <!-- PERSON CARDS LAYER -->
      <div id="cardsLayer"></div>
    </div>

    <!-- FLOATING ZOOM / VIEW CONTROLS -->
    <div class="tree-floating-tools">
      <button onclick="zoomIn()" title="Приблизить">+</button>
      <button onclick="zoomOut()" title="Отдалить">−</button>
      <button onclick="resetZoom()" title="Сбросить масштаб (100%)">1:1</button>
      <button onclick="fitToScreen()" title="Вписать всё древо в экран">⛶</button>
      <button onclick="centerOnRoot()" title="К Николаю (Пробанд)">🎯</button>
    </div>

    <!-- LEGEND -->
    <div class="tree-legend">
      <div style="font-weight: 700; margin-bottom: 0.15rem;">Обозначения связей:</div>
      <div class="legend-item"><div class="legend-line" style="background:#2563eb;"></div> Линия отца (стрелка ♂️)</div>
      <div class="legend-item"><div class="legend-line" style="background:#db2777;"></div> Линия матери (стрелка ♀️)</div>
      <div class="legend-item"><div class="legend-line" style="background:#8b5cf6; border-top:1px dashed #8b5cf6;"></div> Брачный союз 💍</div>
      <div class="legend-item"><div class="legend-line" style="background:#f59e0b;"></div> Выделенная ветвь ⭐</div>
    </div>
  </div>

  <!-- TAB 2: GENERATIONS VIEW -->
  <div id="view-list" class="view-section">
    <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:10px; padding:0.75rem 1.25rem; margin-bottom:1.25rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; box-shadow:var(--shadow);">
      <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
        <span style="font-size:0.88rem; font-weight:700; color:var(--text-main);">Линия предков:</span>
        <button id="btnToggleDirectLineGen" class="pill-btn" onclick="toggleDirectLine()" title="Показать только прямую линию предков" style="font-size:0.82rem; font-weight:600; cursor:pointer;">
          🎯 Прямая линия
        </button>
      </div>
      <div id="genCountBadge" style="font-size:0.8rem; color:var(--text-muted); font-weight:600;">
        Все родственники (197 персон • 20 поколений)
      </div>
    </div>
    <div id="generationsContainer"></div>
  </div>

  <!-- TAB 3: TABLE VIEW -->
  <div id="view-table" class="view-section">
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>№</th>
            <th>ФИО</th>
            <th>Пол</th>
            <th>Поколение</th>
            <th>Рождение</th>
            <th>Смерть</th>
            <th>Место</th>
            <th>Ветвь рода</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- TAB 4: HISTORICAL & ARCHIVAL DOCUMENTS GALLERY -->
  <div id="view-archive" class="view-section">
    <div class="archive-header-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
        <div>
          <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.35rem;">
            <span style="font-size:1.8rem;">🏛️</span>
            <h2 style="margin:0; font-size:1.4rem;">Семейный историко-документальный архив</h2>
          </div>
          <p style="color:var(--text-muted); font-size:0.9rem; margin:0; max-width:850px; line-height:1.5;">
            Подлинные архивные первоисточники, подтверждающие боевой путь и историю защитников Отечества рода: архивные наградные листы и фронтовые приказы ЦАМО РФ, документы участников Первой мировой и Великой Отечественной войн, подлинная красноармейская книжка из музейных фондов.
          </p>
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
          <a href="pdf_документы/Туркин Михаил Николаевич 1906.pdf" target="_blank" class="pill-btn" style="background:#2563eb; color:#fff; border-color:#2563eb; font-size:0.8rem;">📥 Альбом Туркина (19 стр. PDF)</a>
          <a href="pdf_документы/Зиновьев Владимир Семенович 1925.pdf" target="_blank" class="pill-btn" style="background:#db2777; color:#fff; border-color:#db2777; font-size:0.8rem;">📥 Альбом Зиновьева (19 стр. PDF)</a>
        </div>
      </div>

      <!-- FILTER PILLS & SEARCH -->
      <div class="archive-toolbar" style="margin-top:1.25rem; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:0.75rem; border-top:1px solid var(--border-color); padding-top:1rem;">
        <div class="archive-filter-pills" id="archiveFilterPills" style="display:flex; flex-wrap:wrap; gap:0.4rem;">
          <button class="pill-btn active" onclick="filterArchiveCategory('all')">Все материалы ({len(archive_catalog.DOCS_CATALOG)})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('ancient')">📜 Летописи и ревизии XVII–XIX вв. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'ancient'])})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('turkin')">🎖️ Туркин М.Н. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'turkin'])})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_v')">🎖️ Зиновьев В.С. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'zinoviev_v'])})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_s')">🛡️ Зиновьев С.Г. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'zinoviev_s'])})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('shuktomov')">🎖️ Шуктомов А.М. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'shuktomov'])})</button>
          <button class="pill-btn" onclick="filterArchiveCategory('shekhonin')">🎖️ Шехонин М.А. ({len([d for d in archive_catalog.DOCS_CATALOG if d['category'] == 'shekhonin'])})</button>
        </div>
        <div class="archive-search-box" style="position:relative; min-width:240px;">
          <input type="text" id="archiveSearchInput" placeholder="🔍 Поиск по названию или фонду..." oninput="handleArchiveSearch(this.value)" style="width:100%; padding:0.4rem 0.75rem; border-radius:20px; border:1px solid var(--border-color); background:var(--bg-primary); color:var(--text-main); font-size:0.82rem;" />
        </div>
      </div>
    </div>

    <!-- ARCHIVE DOCUMENTS GRID -->
    <div class="archive-grid" id="archiveGrid"></div>
  </div>

  <!-- TAB 5: GEOGRAPHY & HISTORY VIEW -->
  <div id="view-info" class="view-section">
    <!-- OVERVIEW -->
    <div class="info-card" id="info-overview">
      <h2>🌳 О семье и структуре родословного древа</h2>
      <p>Родословное древо составлено на основе уникальных семейных архивных рукописных схем, метрических книг, ревизских сказок и переписей населения XVII–XX веков. Пробандом (исходной точкой древа) является <strong>Николай Вячеславович Туркин</strong> (род. 2024 в г. Чумпхон, Таиланд).</p>
      <p>Родословная объединяет два масштабных географических и культурных пласта, разделенных тысячами километров, но соединенных в одной семье:</p>
      <ul>
        <li><strong>Линия матери (Таиланд, побережье Сиамского залива)</strong>: древние тайские роды <strong>Питак (Pithak, พิทักษ์)</strong>, <strong>Памайтонг (Pamaitong, ป่าไม้ทอง)</strong> и <strong>Чамнианкан (Chamniankan, ชำนาญการ)</strong>. Прабабушка Сай Памайтонг родилась в 1919 году в Таиланде, бабушка Дуангдюан Памайтонг — в 1961 году, мать Парита (Питак) Туркина — в 1997 году.</li>
        <li><strong>Линия отца (Республика Коми, Россия)</strong>: четыре глубокие коренные зырянские (коми) ветви из Усть-Вымского, Сыктывдинского, Сысольского, Прилузского и Княжпогостского уездов. Прямая мужская линия Туркиных непрерывно задокументирована по первоисточникам РГАДА, ГАВО и НА РК на протяжении 15 поколений до начала XVII века — 1608 года (более 416 лет подтвержденной родовой летописи). Линии Шехониных, Шуктомовых, Зиновьевых и Летовых прослежены до XVII–XVIII веков.</li>
      </ul>
    </div>

    <!-- WWII HEROES SECTION -->
    <div class="info-card" id="info-heroes">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:1.6rem;">🎖️</span>
        <h2 style="margin:0;">Защитники Отечества: Герои Великой Отечественной и Первой мировой войн</h2>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.25rem;">
        Документально подтвержденные боевые биографии дедов по архивным материалам Центрального архива Министерства обороны РФ (ЦАМО РФ), Российского государственного военно-исторического архива (РГВИА), музейным фондам и наградным приказам:
      </p>

      <div class="veteran-cards-grid">
        <!-- ТУРКИН МИХАИЛ НИКОЛАЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#2563eb;">Туркин Михаил Николаевич</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">03.11.1906 – 02.09.1993 • с. Коквицы, Коми АССР</div>
              </div>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #bfdbfe; white-space:nowrap;">Поколение V • Прапрадед</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Гвардии старший сержант</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">Командир минометного расчета 82-мм</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Воинские соединения:</strong> 18-я гвардейская механизированная Днестровско-Хинганская Краснознаменная ордена Кутузова II степени бригада (9-й гв. мехкорпус, 6-я гвардейская танковая армия); 45-я мехбригада (5-й мехкорпус).</div>
              <div><strong>Фронты и боевой путь:</strong> Брянский (1942), Юго-Западный (оборона Сталинграда), Западный, 1-й и 2-й Украинские фронты (Румыния, Венгрия, штурм Вены, Прага). <strong>Маньчжурская стратегическая операция (август-сентябрь 1945 г.):</strong> Забайкальский фронт. 800-км марш через пустыню Гоби и хребет Большой Хинган, освобождение Мукдена (Шэньяна), пленение войск японской Квантунской армии.</div>
              <div><strong>Призыв:</strong> Усть-Вымский РВК, Коми АССР. Член ВКП(б) с 1943 г.</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏅 Правительственные боевые награды:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>Орден Славы III степени</strong> (Приказ 18 гв. мехбр № 41/н от 06.06.1945) — <em>за отвагу в боях в Австрии и уличных боях в Вене: расчетом уничтожено 3 станковых пулемета, 20 гитлеровцев, подорвано 3 повозки врага с грузом.</em> Представление подписано комбригом Героем Советского Союза гв. подполковником Овчаровым.</li>
                <li><strong>Медаль «За боевые заслуги»</strong> (Приказ 45 мехбр № 37/н от 03.08.1944) — <em>за бои у дер. Стынка (Румыния) 3–4 июня 1944 г.: расчетом уничтожено до 20 солдат, рассеяно до 2 взводов пехоты.</em></li>
                <li><strong>Участие в разгроме Квантунской армии (Маньчжурия, 1945):</strong> Медаль «За победу над Японией», благодарность Верховного Главнокомандующего И. В. Сталина (приказ № 372 от 23.08.1945 г.), бригаде присвоено почетное звание «Хинганская».</li>
                <li><strong>Медаль «За взятие Вены»</strong> (Указ от 09.06.1945).</li>
                <li><strong>Медаль «За оборону Сталинграда»</strong> (Указ от 22.12.1942).</li>
                <li><strong>Медаль «За победу над Германией в ВОВ»</strong> (Указ от 09.05.1945).</li>
                <li><strong>Нагрудный знак «Отличный минометчик»</strong> (1943).</li>
                <li><strong>Орден Отечественной войны II степени</strong> (Указ от 06.04.1985 к 40-летию Победы).</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>ЦАМО РФ: фонд 33, опись 686196, дело 304; оп. 690155, дело 5198; Юбилейная картотека, шкаф 58, ящик 38. Книга Памяти Республики Коми, т. 6.</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 Сохраненные первоисточники и сканы ЦАМО РФ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <a href="pdf_документы/Туркин Михаил Николаевич 1906.pdf" target="_blank" class="pill-btn" style="font-size:0.74rem;">📥 Полный альбом ЦАМО (19 стр. PDF)</a>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_slava_3')" style="font-size:0.74rem;">🔍 Скан: Орден Славы</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_medal_zaslugi')" style="font-size:0.74rem;">🔍 Скан: Боевые заслуги</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_jbd_3june1944_p26')" style="font-size:0.74rem;">⚔️ ЖБД 45 мбр: Бой 3 июня 1944 г.</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_jbd_3june1944_crop')" style="font-size:0.74rem;">🎯 Фрагмент: Подвиг минометчиков</button>
                <button class="pill-btn active" onclick="openDocViewerById('turkin_kniga_pamyati')" style="font-size:0.74rem;">📖 Скан: Книга Памяти РК</button>
                <button class="pill-btn" onclick="filterArchiveCategory('turkin'); switchTab('archive');" style="font-size:0.74rem;">📁 Все 13 документов ЦАМО</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I19'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>

        <!-- ТУРКИН ИВАН НИКОЛАЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#2563eb;">Туркин Иван Николаевич</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">род. 1918 • д. Сюлатуй (Коквицы), Коми АССР</div>
              </div>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #bfdbfe; white-space:nowrap;">Поколение V • Брат Михаила</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Красноармеец</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">Участник Великой Отечественной войны</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Родство:</strong> Младший сын Николая Алексеевича Туркина и Павлы Ивановны Сизевой, родной брат Михаила Николаевича Туркина. Двоюродный прадедушка.</div>
              <div><strong>Место рождения:</strong> Коми АССР, Усть-Вымский район, Коквицкий сельсовет, деревня Сюлатуй (Сюлатуйская).</div>
              <div><strong>Призыв:</strong> Призван по мобилизации в июне 1941 года Сыктывкарским ГВК Коми АССР.</div>
              <div><strong>Значение для родословной:</strong> Документально подтверждает неразрывность связи селений Сюлатуй и Коквицы в роду Туркиных.</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#2563eb; margin-bottom:0.4rem;">📖 Архивные источники:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li>Книга Памяти Республики Коми, том 6, стр. 343.</li>
                <li>Общероссийская база ветеранов и участников Великой Отечественной войны.</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>Сыктывкарский ГВК Коми АССР, июнь 1941 г.</em>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I68'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>

        <!-- ЗИНОВЬЕВ ВЛАДИМИР СЕМЕНОВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #ec489933; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#db2777;">Зиновьев Владимир Семенович</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">род. 1925 • д. Горелый Ыб (с. Горесоит), Коми АССР</div>
              </div>
              <span style="background:#fff1f2; color:#db2777; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fecdd3; white-space:nowrap;">Поколение IV • Брат Альбины</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Старший сержант</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">Командир минометного расчета 1-й минроты</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Родство:</strong> Сын Семена Григорьевича Зиновьева и Клавдии Ильиничны Кызъюровой, родной старший брат прабабушки Альбины Семеновны Гладышевой (Зиновьевой). Двоюродный дедушка Николая.</div>
              <div><strong>Воинские соединения:</strong> 951-й стрелковый полк 265-й стрелковой Выборгской дивизии (7-й стрелковый корпус, 3-я ударная армия, 1-й Белорусский фронт; ранее — Ленинградский и 3-й Прибалтийский фронты).</div>
              <div><strong>Боевой путь:</strong> В армии со 2 января 1943 г. (призван в 17 лет). В боях с 19 февраля 1943 г., ранен 20 февраля 1943 г. Бои на Карельском перешейке против финских войск, освобождение Прибалтики, Висло-Одерская операция, освобождение Варшавы и штурм Берлина.</div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏅 Правительственные боевые награды:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>Орден Красной Звезды</strong> (Приказ 265 сд № 18/н от 06.03.1945) — <em>в оборонительном бою севернее н.п. Хасендорф 18.02.1945 г., командуя расчетом, уничтожил 19 солдат и пулемет противника.</em></li>
                <li><strong>Орден Славы III степени</strong> (Приказ 265 сд № 80/н от 27.09.1944) — <em>в бою у н.п. Вилтой 19.09.1944 г. расчет подавил 2 станковых пулемета и миномет, отразил 2 вражеские контратаки.</em></li>
                <li><strong>Медаль «За отвагу»</strong> (Приказ 951 сп № 016-Н от 15.07.1944) — <em>за бои на Карельском перешейке: под ураганным огнем работал за наводчика и заряжающего.</em></li>
                <li><strong>Медаль «За взятие Берлина»</strong> (Акт от 09.06.1945).</li>
                <li><strong>Медаль «За освобождение Варшавы»</strong> (Акт от 09.06.1945).</li>
                <li><strong>Медаль «За победу над Германией в ВОВ»</strong> (09.05.1945).</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>ЦАМО РФ: фонд 33, опись 686196, дело 1311; оп. 687572, дело 2112; оп. 690155, дело 1302; шкаф 35, ящик 8.</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 Сохраненные первоисточники и сканы ЦАМО РФ:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <a href="pdf_документы/Зиновьев Владимир Семенович 1925.pdf" target="_blank" class="pill-btn" style="font-size:0.74rem;">📥 Полный альбом ЦАМО (19 стр. PDF)</a>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_red_star')" style="font-size:0.74rem;">🔍 Скан: Красная Звезда</button>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_slava_3')" style="font-size:0.74rem;">🔍 Скан: Орден Славы</button>
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_v_otvaga_list')" style="font-size:0.74rem;">🔍 Скан: За отвагу</button>
                <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_v'); switchTab('archive');" style="font-size:0.74rem;">📁 Все 9 сканов ЦАМО</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I67'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>

        <!-- ЗИНОВЬЕВ СЕМЕН ГРИГОРЬЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #ec489933; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#db2777;">Зиновьев Семён Григорьевич</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">27.01.1890 – ? • д. Горелый Ыб (Ибская), Коми АССР</div>
              </div>
              <span style="background:#fff1f2; color:#db2777; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fecdd3; white-space:nowrap;">Поколение V • Прапрадед</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Унтер-офицер РИА</span>
              <span class="badge-veteran">Старший артиллерист РККА</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">Ветеран двух мировых войн (ПМВ и ВОВ)</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Родство:</strong> Муж Клавдии Ильиничны Кызъюровой, отец героя штурма Берлина Владимира Семеновича Зиновьева и прабабушки Альбины Семеновны Гладышевой (Зиновьевой). Прапрадедушка Николая.</div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>⚔️ Первая мировая война (1914–1918):</strong>
                Унтер-офицер (ранее ефрейтор) 181-го пехотного Остроленского полка (46-я пехотная дивизия, 21-й армейский корпус). Участник Галицийской битвы и Краковской операции. В боях под Краковом (Ковали, Костелец, Циборовице) 8–13 ноября 1914 г. пропал без вести; взят в плен 21.12.1914 г. С 15.01.1915 г. содержался в лагере военнопленных Миловиц (Milowitz, Австро-Венгрия, ныне Чехия). После войны вернулся на родину в Коми край.
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🛡️ Великая Отечественная война (1941–1945):</strong>
                Старший артиллерист 7-й роты 2-го стрелкового батальона 34-го запасного стрелкового полка. Призван в действующую армию в возрасте 53 лет (1943 г.).
              </div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b91c1c; margin-bottom:0.4rem;">🏛️ Документы и музейные источники:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>Красноармейская книжка от 13.06.1943 г.</strong> («Годен к … 7.8.44») — Айкинский центральный музей Усть-Вымского музейного объединения Республики Коми, КП 8347, рег. № 21112145.</li>
                <li><strong>Именной список потерь 181 пехотного Остроленского полка № 31904</strong> — РГВИА, ф. 16196, оп. 1, д. 346.</li>
                <li><strong>Карточка военнопленного лагеря Миловиц (Milowitz)</strong> — РГВИА, Картотека бюро учета потерь (пленные), шкаф б/н, ящик 6292-К.</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>РГВИА: фонд 16196, опись 1, дело 346; Ящик 6292-К. Айкинский центральный музей МБУ «Усть-Вымское ММО».</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 Сохраненные первоисточники и архивные дела:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('zinoviev_s_krasnoarm_knizhka')" style="font-size:0.74rem;">🔍 Скан: Красноармейская книжка 1943 г.</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_plen_card_front')" style="font-size:0.74rem;">🛡️ Скан: Карточка военнопленного (1915 г.)</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_plen_card_back')" style="font-size:0.74rem;">📄 Оборот карточки военнопленного</button>
                <button class="pill-btn" onclick="openDocViewerById('zinoviev_s_spisok_poter_1914')" style="font-size:0.74rem;">⚔️ Скан: Список потерь 181-го полка (1914 г.)</button>
                <button class="pill-btn" onclick="filterArchiveCategory('zinoviev_s'); switchTab('archive');" style="font-size:0.74rem;">📁 Все 4 документа в архиве</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I25'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>

        <!-- ШУКТОМОВ АЛЕКСАНДР МИХАЙЛОВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#b45309;">Шуктомов Александр Михайлович</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">1911 – сентябрь 1970 • д. Ероздино, Коми АССР</div>
              </div>
              <span style="background:#fef3c7; color:#b45309; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fde68a; white-space:nowrap;">Поколение V • Прапрадед</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Рядовой РККА</span>
              <span class="badge-veteran">34-й запасной стрелковый полк</span>
              <span style="background:var(--bg-surface); border:1px solid var(--border-color); font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:600;">Участник Великой Отечественной войны</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Родство:</strong> Муж Агнии Ивановны Шуктомовой (Пасынковой), отец Риммы Александровны Туркиной (Шуктомовой). Прапрадедушка Николая.</div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🛡️ Великая Отечественная война (1941–1945):</strong>
                Призван по мобилизации Усть-Вымским РВК Коми АССР в декабре 1941 г. Проходил подготовку рядовым стрелком в 5-й стрелковой роте 2-го батальона 34-го запасного стрелкового полка (34 зсп 29 зсд). 18 января 1942 г. с маршевой командой № 43 направлен на фронт в действующую армию. Демобилизован в июле 1942 г. Умер в сентябре 1970 г. в возрасте 59 лет.
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🤝 Историческая перекличка:</strong>
                Проходил службу в том же 34-м запасном стрелковом полку (34 зсп 29 зсд), где служил старшим артиллеристом другой предок — Семён Григорьевич Зиновьев.
              </div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#b45309; margin-bottom:0.4rem;">🏛️ Архивные документы и первоисточники:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>Именной список военно-пересыльного пункта 34 зсп 29 зсд от 18.01.1942 г.</strong> — ЦАМО РФ, фонд 8312, опись 37579с, дело 3, кадр 38, запись № 3526.</li>
                <li><strong>Печатная Книга Памяти Республики Коми</strong> — том 6, стр. 705 (сведения о призыве, демобилизации в июле 1942 г. и дате смерти в сентябре 1970 г.).</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>ЦАМО РФ: фонд 8312 (34 запасной стрелковый полк 29 зсд), опись 37579с, дело 3; Книга Памяти Республики Коми (том 6).</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 Сохраненные первоисточники и архивные дела:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('shuktomov_vpp_1942')" style="font-size:0.74rem;">🔍 Скан: Список 34 зсп (18.01.1942 г.)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shuktomov_kniga_pamyati_komi')" style="font-size:0.74rem;">📖 Скан: Книга Памяти РК (том 6)</button>
                <button class="pill-btn" onclick="filterArchiveCategory('shuktomov'); switchTab('archive');" style="font-size:0.74rem;">📁 Все 2 документа в архиве</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I23'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>

        <!-- ШЕХОНИН МИХАИЛ АФАНАСЬЕВИЧ -->
        <div class="veteran-card" style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #8b5cf633; padding:1.25rem; box-shadow:var(--shadow);">
          <div>
            <div class="veteran-card-header">
              <div>
                <h3 style="margin:0; font-size:1.15rem; color:#7c3aed;">Шехонин Михаил Афанасьевич</h3>
                <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">1909 – ноябрь 1988 • с. Лойма, Коми АССР</div>
              </div>
              <span style="background:#f5f3ff; color:#7c3aed; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #ddd6fe; white-space:nowrap;">Поколение V • Прапрадед</span>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.85rem;">
              <span class="badge-veteran">Младший лейтенант РККА</span>
              <span class="badge-veteran">995-й стрелковый полк (263 сд)</span>
              <span style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:0.75rem; padding:0.15rem 0.45rem; border-radius:4px; font-weight:700;">🎖️ Орден Отечественной войны I степени</span>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; margin-bottom:0.85rem;">
              <div><strong>Родство:</strong> Муж Марии Степановны Сюткиной, отец Зинаиды Михайловны Туркиной (Шехониной), дедушка Аркадия Туркина. Прапрадедушка Николая по линии матери дедушки.</div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🛡️ Великая Отечественная война (1941–1945):</strong>
                Призван по мобилизации Прилузским РВК Коми АССР в июле 1941 г. Офицер Красной армии (воинское звание — младший лейтенант). Проходил службу в 995-м стрелковом полку 263-й стрелковой дивизии на Карельском фронте. В кровопролитных боях получил тяжелое боевое ранение.
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🏥 Госпитальные этапы и демобилизация:</strong>
                Проходил лечение в 25-м отдельном медико-санитарном батальоне (25 медсб 263 сд), затем эвакуирован в тыловые эвакогоспитали ЭГ 1438 / 1439 и ЭГ 2513. 25 января 1943 года выбыл из госпиталя и был демобилизован по ранению.
              </div>
              <div style="margin-top:0.35rem; padding-top:0.35rem; border-top:1px dashed var(--border-color);">
                <strong>🎖️ Награда за подвиг и ранение:</strong>
                Указом Президиума Верховного Совета СССР награжден <strong>Орденом Отечественной войны I степени</strong> (Приказ МО СССР № 89 от 06.04.1985 г.). Скончался в ноябре 1988 года в родном селе Лойма в возрасте 79 лет.
              </div>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.85rem; margin-bottom:0.85rem;">
              <div style="font-weight:700; font-size:0.86rem; color:#7c3aed; margin-bottom:0.4rem;">🏛️ Архивные документы и первоисточники:</div>
              <ul style="margin:0; padding-left:1.2rem; font-size:0.83rem; line-height:1.55;">
                <li><strong>Печатная Книга Памяти Республики Коми</strong> — том 5, стр. 612 (сведения о рождении, звании мл. лейтенанта, призыве в июле 1941 г., демобилизации по ранению в январе 1943 г. и смерти в ноябре 1988 г. в с. Лойма).</li>
                <li><strong>Филиал ЦАМО РФ (военно-медицинских документов, г. Санкт-Петербург)</strong> — Картотека общего учета, шкаф Шеряев - Шишера, ящик 096-26; Фонд «Свидетельства о болезни», ящик ЭГ 2513.</li>
                <li><strong>ЦАМО РФ</strong> — Юбилейная картотека награждений, шкаф 62, ящик 2, номер документа 89 (Орден Отечественной войны I ст., запись № 1522835818).</li>
              </ul>
            </div>

            <div style="font-size:0.75rem; color:var(--text-muted); line-height:1.4;">
              📚 <em>ЦАМО РФ: Юбилейная картотека (шкаф 62, ящик 2); Филиал ЦАМО (ВМД): ящик 096-26, ЭГ 2513; Книга Памяти Республики Коми (том 5, стр. 612).</em>
            </div>

            <div style="background:var(--bg-surface); border:1px solid var(--border-color); border-radius:8px; padding:0.65rem 0.85rem; margin-top:0.75rem; font-size:0.8rem;">
              <div style="font-weight:700; color:var(--accent); margin-bottom:0.35rem;">📁 Сохраненные первоисточники и архивные дела:</div>
              <div style="display:flex; flex-wrap:wrap; gap:0.4rem;">
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_kniga_pamyati_komi_full')" style="font-size:0.74rem;">📖 Скан: Книга Памяти (том 5, стр. 612)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_kniga_pamyati_komi_crop')" style="font-size:0.74rem;">🔍 Скан: Именная статья (фрагмент)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_card_ranenie_vmd')" style="font-size:0.74rem;">🏥 Карточка: Ранения и госпитали (ЦАМО ВМД)</button>
                <button class="pill-btn active" onclick="openDocViewerById('shekhonin_yubileinaya_kartoteka_1985')" style="font-size:0.74rem;">🎖️ Награда: Орден Отеч. войны I ст.</button>
                <button class="pill-btn" onclick="filterArchiveCategory('shekhonin'); switchTab('archive');" style="font-size:0.74rem;">📁 Все 4 документа в архиве</button>
              </div>
            </div>
          </div>
          <div style="margin-top:0.85rem; padding-top:0.6rem; border-top:1px solid var(--border-color);">
            <button class="pill-btn" onclick="focusPerson('I21'); switchTab('tree');" style="font-size:0.78rem;">🎯 Найти на древе</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ORTHODOX CLERGY & PARISH CHURCHES SECTION -->
    <div class="info-card" id="info-clergy">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
        <span style="font-size:1.6rem;">⛪</span>
        <h2 style="margin:0;">Православное духовенство и приходские храмы предков (XVII–XX вв., 1646–1937 гг.)</h2>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:1.2rem; line-height:1.55;">
        На протяжении более трёх столетий — от переписных книг XVII века до XX века — духовная и повседневная жизнь всех поколений предков была неразрывно связана с православными обителями и приходскими церквями Яренского, Усть-Вымского и Усть-Сысольского уездов Вологодской губернии (ныне Республика Коми и Кировская область). Род Туркиных дал Северу уникальную династию священнослужителей, соборных диаконов, причетников и монашествующих, а все родственные семьи (Шуктомовы, Зиновьевы, Сюткины, Полещиковы, Пасынковы, Кызъюровы, Летовы, Ярановы) на протяжении веков принимали в этих храмах таинства крещения, браковенчания и погребения.
      </p>

      <!-- STATS BANNER -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:0.75rem; margin-bottom:1.35rem;">
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#2563eb;">Почти 300 лет</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">служения и исповедничества (1646–1937 гг.)</div>
        </div>
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#7c3aed;">10 обителей и храмов</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">Коквицы, Усть-Вымь, Лальск, Ульяново, Ыб, Лойма, Ляли, Оквад, Палевицы, Яренск</div>
        </div>
        <div style="background:var(--bg-primary); border:1px solid var(--border-color); border-radius:8px; padding:0.75rem 1rem; text-align:center;">
          <div style="font-size:1.35rem; font-weight:800; color:#0284c7;">30+ служителей</div>
          <div style="font-size:0.76rem; color:var(--text-muted); margin-top:0.2rem;">священники, диаконы, монахи, дьячки, пономари и приказные</div>
        </div>
      </div>

      <!-- CHURCHES SUMMARY GRID WITH PHOTOS -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.15rem;">
        
        <!-- КОКВИЦЫ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #2563eb33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#2563eb;">🏛️ с. Коквицы — Христорождественская церковь</h3>
              <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bfdbfe;">Главный оплот рода (150+ лет)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Коквицкая гора, Яренский уезд • Приход родов: Туркины, Летовы, Ярановы, Сизевы</div>
            
            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png" target="_blank" title="Исповедная роспись 1773 г., двор 167 священника о. Степана Туркина (нажмите для открытия)">
                <img src="архив_сканы_первоисточников/1773_Коквицы_двор_167_crop.png" alt="Исповедная роспись 1773 г., Коквицы" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>📜 Каменная двухэтажная церковь построена в 1820–1837 гг. (ранее деревянный храм XVII–XVIII вв.).</div>
                <div style="margin-top:0.35rem;">👶 В метрической книге прихода зафиксировано рождение прапрадеда <strong>Николая Алексеевича Туркина</strong> 3 ноября 1876 г. (д. Сюлатуй, запись на с. 267).</div>
              </div>
            </div>

            <p style="font-size:0.83rem; line-height:1.5; margin-bottom:0.65rem;">Родовое гнездо и непрерывное служение нескольких поколений клира Туркиных:</p>
            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>Священники (иереи):</strong> о. Степан Иванович Туркин (служил в 1734–1773 гг., разбор 1736 г., в 1773 г. 62-летний вдовый священник по исповедной росписи ВЦА двор 167); о. Иван Петрович Туркин (пономарь в 1710 г., священник в 1747 г.).</li>
              <li><strong>Диаконы:</strong> о. Алексей Елисеевич Туркин (пономарь с 1818 г., рукоположен в диакона в 1822 г., служил до 1844+ гг.).</li>
              <li><strong>Пономари:</strong> Леонтий Петрович (1732–1783 гг.); Елисей Леонтьевич (посвящен в 1783 г. еп. Иоанном, служил более 33 лет, супруга Татьяна Васильевна Пономарёва); Пётр Петрович (~1714 г.р.).</li>
              <li><strong>Сыновья причта:</strong> Иван (пономарь), Максим, Гавриил, Дмитрий (РС 1795 и 1811 гг.).</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I78'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Степан</button>
            <button class="pill-btn" onclick="focusPerson('I234'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Алексей</button>
            <button class="pill-btn" onclick="focusPerson('I232'); switchTab('tree');" style="font-size:0.74rem;">🎯 Елисей</button>
          </div>
        </div>

        <!-- ЛАЛЬСК -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #8b5cf633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#7c3aed;">⛪ г. Лальск — Воскресенский собор</h3>
              <span style="background:#f5f3ff; color:#7c3aed; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #ddd6fe;">Соборный диакон (1870–1904)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">г. Лальск, Вологодская епархия (ныне Кировская область) • Шедевр барокко 1698–1715 гг.</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Лальск_Воскресенский_собор.jpg" target="_blank" title="Воскресенский собор в Лальске (архивное фото С. Лобовикова конца XIX в., нажмите для увеличения)">
                <img src="фото_храмов/Лальск_Воскресенский_собор.jpg" alt="Воскресенский собор г. Лальска" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🏛️ Величественный пятиглавый соборный ансамбль с шатровой колокольней.</div>
                <div style="margin-top:0.35rem;">📜 Снимок сделан выдающимся русским фотографом С. Лобовиковым именно в годы соборного служения о. Михаила Туркина.</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>Соборный диакон о. Михаил Алексеевич Туркин</strong> (ок. 1839 – 14.06.1904) — сын диакона о. Алексея Коквицкого. Выпускник Вологодской духовной семинарии (1862 г.). С 1868 г. дьячок, 20.07.1870 г. рукоположен во диакона, с 1871 г. — штатный соборный диакон (34 года беспорочного служения, фонд ГАКО № 1310). Супруга София Прокопьевна Брызгалова.</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I236'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Михаил Лальский</button>
          </div>
        </div>

        <!-- УЛЬЯНОВСКИЙ МОНАСТЫРЬ И С. КУЖБА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #6366f133; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#4f46e5;">⛪ с. Ульяново и с. Кужба — Троице-Стефановский монастырь</h3>
              <span style="background:#eef2ff; color:#4f46e5; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #c7d2fe;">Исповедники XX века</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Усть-Сысольский и Усть-Куломский уезды • Верхняя Вычегда • 1865–1937 гг.</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Ульяново_Троице_Стефановский_монастырь.jpg" target="_blank" title="Троице-Стефано-Ульяновский мужской монастырь (нажмите для увеличения)">
                <img src="фото_храмов/Ульяново_Троице_Стефановский_монастырь.jpg" alt="Троице-Стефано-Ульяновский монастырь" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🌲 Знаменитая северная обитель, основанная святителем Стефаном Пермским в конце XIV в. и возрожденная в XIX в.</div>
                <div style="margin-top:0.35rem;">⚖️ Архивно-следственное дело УНКВД Коми АССР 1937 г. (Архив УФСБ по РК, № КП-7444).</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>Монах Виталий (Виталий Иванович Туркин)</strong> (1865, с. Коквицы – 06.11.1937) — родной брат прапрапрадеда Алексея Ивановича Туркина и дядя Николая Алексеевича Туркина. Монах Троице-Стефано-Ульяновского мужского монастыря. После закрытия обители в 1923 г. проживал в с. Кужба вместе с казначеем обители священномучеником иеромонахом Мелетием (Федюнёвым), тайно совершая требы для верующих. Арестован в сентябре 1937 г., приговорён «тройкой» к 10 годам ИТЛ, мученически погиб в Вогваздинском лагпункте Ухтпечлага. Реабилитирован.</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I307'); switchTab('tree');" style="font-size:0.74rem;">🎯 монах Виталий</button>
          </div>
        </div>

        <!-- ЫБ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #05966933; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ с. Ыб — Свято-Вознесенский храм</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">Приход предков (1827–1835)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Село Ыб (Ыбский приход) • Сыктывдинский район • Памятник зодчества XIX века</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Ыб_Вознесенская_церковь.jpg" target="_blank" title="Свято-Вознесенская церковь в селе Ыб (нажмите для увеличения)">
                <img src="фото_храмов/Ыб_Вознесенская_церковь.jpg" alt="Вознесенский храм в с. Ыб" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🏛️ Монументальный каменный храм с высокой колокольней, воздвигнутый в 1827–1835 гг.</div>
                <div style="margin-top:0.35rem;">💍 Родовой духовный центр предков по линии бабушки Риммы Александровны Туркиной: родов <strong>Зиновьевых, Пасынковых, Кызъюровых, Айбабиных</strong>.</div>
              </div>
            </div>

            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>Метрики таинств (НАРК ф. 130):</strong> здесь венчались Харлампий Яковлевич Пасынков и Параскева Круглякова (24.04.1846 г.); Иван Григорьевич Кызъюров и Александра Шилина (18.01.1859 г.); Платон Харлампиевич Пасынков и Анастасия Каракчиева (10.11.1874 г.).</li>
            </ul>
          </div>
        </div>

        <!-- ЛОЙМА -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #d9770633; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ с. Лойма — Церковь Успения Богородицы</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">Приход рода Сюткиных</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Прилузский район • Река Луза • Построена в 1802–1804 гг. • Росписи 1916 г.</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Лойма_Успенская_церковь.jpg" target="_blank" title="Церковь Успения Богородицы в с. Лойма (нажмите для увеличения)">
                <img src="фото_храмов/Лойма_Успенская_церковь.jpg" alt="Успенская церковь в с. Лойма" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🎨 Каменный храм с тёплым и холодным приделами Афанасия и Кирилла Александрийских. Сохранил росписи васнецовской школы 1916 г.</div>
                <div style="margin-top:0.35rem;">🌾 Приходской храм прапрабабушки <strong>Марии Степановны Сюткиной</strong> (1911–1981), её отца Степана Петровича Сюткина (1880–1933) и деда Петра Сюткина.</div>
              </div>
            </div>
          </div>
        </div>

        <!-- УСТЬ-ВЫМЬ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #10b98133; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#059669;">⛪ с. Усть-Вымь — Михайло-Архангельский монастырь и храмы</h3>
              <span style="background:#ecfdf5; color:#059669; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #a7f3d0;">Прямой предок (1731 г.)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Усть-Вымская волость • Кафедральный духовный центр св. Стефана Пермского</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Усть_Вымь_Михайло_Архангельский_храм.jpg" target="_blank" title="Усть-Вымский ансамбль (нажмите для увеличения)">
                <img src="фото_храмов/Усть_Вымь_Михайло_Архангельский_храм.jpg" alt="Усть-Вымский Михайло-Архангельский ансамбль" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🏛️ Исторический кафедральный центр Пермской епархии на слиянии рек Выми и Вычегды.</div>
                <div style="margin-top:0.35rem;">📜 Здесь в Благовещенской церкви в 1731 г. служил священник <strong>о. Пётр Исаакович Туркин</strong> (прямой 8-й прадедушка, МК ГААО ф. 29, оп. 27, д. 1, л. 40).</div>
              </div>
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I72'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Пётр Исаакович</button>
          </div>
        </div>

        <!-- ЛЯЛИ -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #ec489933; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#db2777;">⛪ с. Ляли — Богоявленская церковь</h3>
              <span style="background:#fdf2f8; color:#db2777; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fbcfe8;">Клир и приход предков</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Княжпогостский район • Река Вымь • Памятник зодчества 1852–1856 гг.</div>

            <div style="display:flex; gap:0.85rem; margin-bottom:0.75rem; align-items:flex-start;">
              <a href="фото_храмов/Ляли_Богоявленская_церковь.jpg" target="_blank" title="Богоявленская церковь в с. Ляли (нажмите для увеличения)">
                <img src="фото_храмов/Ляли_Богоявленская_церковь.jpg" alt="Богоявленская церковь в с. Ляли" style="width:115px; height:130px; object-fit:cover; border-radius:6px; border:1px solid var(--border-color); box-shadow:0 2px 6px rgba(0,0,0,0.1); cursor:pointer; transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; line-height:1.45; color:var(--text-main);">
                <div>🏰 Каменный храм на древнем торговом пути по реке Вымь.</div>
                <div style="margin-top:0.35rem;">🔔 Здесь служил дьячком <strong>Симеон Алексеевич Туркин</strong> (1822–1847 гг.). Также являлся родовым приходом семей <strong>Каракчиевых</strong> и <strong>Шилиных</strong>.</div>
              </div>
            </div>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I235'); switchTab('tree');" style="font-size:0.74rem;">🎯 Симеон Ляльский</button>
          </div>
        </div>

        <!-- ОКВАД -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #0284c733; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#0284c7;">⛪ погост Оквад (Катвад) — Введенская церковь</h3>
              <span style="background:#f0f9ff; color:#0284c7; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #bae6fd;">Колыбель рода (XVII в.)</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Оквадская волость, Яренский уезд • XVII–XVIII вв.</div>
            <p style="font-size:0.83rem; line-height:1.5; margin-bottom:0.65rem;">Древнейшее задокументированное местопребывание рода Туркиных на Вычегде:</p>
            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>Основатель династии:</strong> Афанасий Семёнович Туркин (ок. 1600 г.р.) — архиепископский приказной человек на Коквицком погосте по переписи 1646 г. (РГАДА ф. 1209, д. 1080), управлял вотчинными доходами архиепископа Вологодского и Великопермского.</li>
              <li><strong>Дьячки и пономари:</strong> Исаакий Афанасьевич Туркин (род. 1635 г., 11 лет в 1646 г.) — дьячок Введенской церкви (переписная книга 1678 г.), пономарь (1696/97 г.).</li>
              <li><strong>Священники:</strong> о. Автоном Лаврентьевич Туркин (ок. 1690 г.р.) — священник Введенской церкви в 1731 и 1736 гг. (МК ГААО ф. 29, разбор ВУЦА ф. 363), дочь Марина.</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.74rem;">🎯 Афанасий</button>
            <button class="pill-btn" onclick="focusPerson('I73'); switchTab('tree');" style="font-size:0.74rem;">🎯 Исаакий</button>
            <button class="pill-btn" onclick="focusPerson('I245'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Автоном</button>
          </div>
        </div>

        <!-- ПАЛЕВИЦЫ И ДР. -->
        <div style="background:var(--bg-primary); border-radius:10px; border:1.5px solid #f59e0b33; padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between; box-shadow:var(--shadow);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <h3 style="margin:0; font-size:1.05rem; color:#d97706;">⛪ Палевицы, Серёгово, Яренск</h3>
              <span style="background:#fffbeb; color:#d97706; font-weight:700; font-size:0.72rem; padding:0.15rem 0.5rem; border-radius:6px; border:1px solid #fde68a;">Приходы Вычегды</span>
            </div>
            <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.65rem;">Палевицы, Серёгово, Княжпогост, соборы г. Яренска</div>
            <ul style="font-size:0.82rem; line-height:1.5; margin:0 0 0.75rem 0; padding-left:1.15rem;">
              <li><strong>с. Палевицы (Покровская ц.):</strong> священник о. Алексей Тимофеевич Туркин (1734–1758 гг., супруга Матрона, дети Михаил, Андрей, Марфа); дьячок Иван Петрович Туркин (1747 г.).</li>
              <li><strong>с. Серёгово и Княжпогост:</strong> пономарь и дьячок Иван Елисеевич Туркин (1802–1815+ гг.).</li>
              <li><strong>г. Яренск (Преображенский собор):</strong> соборный сторож Михаил Алексеевич Туркин (с 1755 г., жена Марфа Козьминична (Ипатова)).</li>
            </ul>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:0.35rem; border-top:1px dashed var(--border-color); padding-top:0.5rem;">
            <button class="pill-btn" onclick="focusPerson('I239'); switchTab('tree');" style="font-size:0.74rem;">🎯 о. Алексей</button>
            <button class="pill-btn" onclick="focusPerson('I238'); switchTab('tree');" style="font-size:0.74rem;">🎯 Иван</button>
            <button class="pill-btn" onclick="focusPerson('I241'); switchTab('tree');" style="font-size:0.74rem;">🎯 Михаил</button>
          </div>
        </div>

      </div>

      <!-- CONSOLIDATED ARCHIVE FUNDS & SACRAMENTS BLOCK -->
      <div style="background:var(--bg-surface); border-radius:10px; border:1.5px solid var(--border-color); padding:1.25rem; margin-top:1.25rem; box-shadow:var(--shadow);">
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.75rem;">
          <span style="font-size:1.35rem;">📜</span>
          <h3 style="margin:0; font-size:1.1rem; color:var(--text-main);">Сводные архивные фонды и метрические свидетельства таинств предков</h3>
        </div>
        <p style="font-size:0.85rem; line-height:1.6; color:var(--text-muted); margin-bottom:1rem;">
          Все поколения предков были прихожанами старинных северных церквей Усть-Сысольского, Усть-Вымского и Яренского уездов Вологодской губернии. Их метрические книги, исповедные ведомости и ревизские сказки сосредоточены в государственных архивах:
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1rem;">
          <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color); font-size:0.83rem; line-height:1.55;">
            <div style="font-weight:700; color:#2563eb; margin-bottom:0.45rem; font-size:0.88rem;">💍 Документально подтвержденные браковенчания предков:</div>
            <ul style="margin:0; padding-left:1.15rem;">
              <li><strong>24 апреля 1846 г.:</strong> Харлампий Яковлевич Пасынков (19 лет) обвенчался с девицей Параскевой Ивановной Кругляковой (18 лет) в Вознесенском приходе с. Ыб.</li>
              <li><strong>24 января 1858 г.:</strong> Иван Иванович Поздеев (23 года) обвенчался с девицей Синклитикией Ионичной Каракчиевой (17 лет) в приходе д. Ероздино / с. Ыб.</li>
              <li><strong>18 января 1859 г.:</strong> Иван Григорьевич Кызъюров (23 года) обвенчался с девицей Александрой Николаевной Шилиной (20 лет) в приходе с. Малый Ыб.</li>
              <li><strong>10 ноября 1874 г.:</strong> Платон Харлампиевич Пасынков обвенчался с девицей Анастасией Андреевной Каракчиевой («венец 10.11.1874») в приходе с. Ыб.</li>
            </ul>
          </div>

          <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color); font-size:0.83rem; line-height:1.55;">
            <div style="font-weight:700; color:#059669; margin-bottom:0.45rem; font-size:0.88rem;">🏛️ Государственные архивные фонды:</div>
            <ul style="margin:0; padding-left:1.15rem;">
              <li><strong>НАРК (Сыктывкар):</strong> Ф. 231 (ревизские сказки 1816, 1834, 1850 гг.), Ф. 254 (МК Коквицкой церкви), Ф. 130 (МК Вознесенского собора с. Ыб).</li>
              <li><strong>ГАВО (Вологда):</strong> Ф. 388 (8-я ревизия 1834 г. Усть-Вымской волости, семья № 43 Туркиных; клировые ведомости).</li>
              <li><strong>ВЦА (Великий Устюг):</strong> Ф. 363 (Исповедная роспись 1773 г., двор 167 священника о. Степана Туркина).</li>
              <li><strong>РГАДА (Москва):</strong> Ф. 1209 (переписи 1646 и 1678 гг. Оквада и Коквиц), Ф. 350 (2-я ревизия 1748 г. по д. Палтыдор рода Летовых).</li>
              <li><strong>ГААО (Архангельск):</strong> Ф. 29, оп. 27, д. 1 (МК Усть-Вымской Благовещенской церкви 1731 г. священника о. Петра Туркина).</li>
              <li><strong>ГАКО (Киров):</strong> Ф. 1310 (послужные списки соборного диакона о. Михаила Туркина).</li>
              <li><strong>Архив УФСБ по РК:</strong> Дело № КП-7444 (1937 г., монах Виталий Туркин, Ульяновский монастырь).</li>
            </ul>
          </div>
        </div>
      </div>

    </div>

    <!-- GEOGRAPHY SECTION -->
    <div class="info-card" id="info-geography">
      <h2>🗺️ Историческая география селений и городов рода</h2>
      <p style="color:var(--text-muted); margin-bottom:1.25rem;">Селения расположены в бассейнах великих рек Русского Севера (Сысолы, Вычегды, Выми, Лузы) и на юге Сиама:</p>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem;">
        <!-- ЫБ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:var(--accent); margin-bottom:0.35rem;">🏛️ Село Ыб (Ибы, Малый Ыб)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Сыктывдинский район • Река Сысола • Известно с 1586 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Один из древнейших культурных и сакральных центров Коми края, расположенный на семи холмах вдоль реки Сысолы. Название происходит от коми слова <em>«ыб»</em> — возвышенность, суходольное поле на холме. Родовое гнездо многих поколений <strong>Туркиных, Зиновьевых, Пасынковых, Кызъюровых и Айбабиных</strong>. В селе действовала каменная Свято-Вознесенская церковь (освящена в 1827–1835 гг., НАРК ф. 130) и более десятка святых целебных источников.</p>
        </div>

        <!-- ГОРЕЛЫЙ ЫБ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#ec4899; margin-bottom:0.35rem;">🌲 Деревня Горелый Ыб (с. Горесоит)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Серегово-Горская волость • Река Вымь</div>
          <p style="font-size:0.86rem; line-height:1.5;">Старинное селение Сереговских гор на реке Вымь. Историческая родина ветвей <strong>Кызъюровых и Зиновьевых</strong>. Здесь родились прапрабабушка Клавдия Ильинична Кызъюрова (род. 1900), герой войны Владимир Семенович Зиновьев (род. 1925), а также советский государственный деятель, председатель Коми облисполкома (1937–1938) Иона Алексеевич Кызъюров.</p>
        </div>

        <!-- ЛОЙМА -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#8b5cf6; margin-bottom:0.35rem;">🌾 Село Лойма</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Прилузский район • Река Луза (Лузская Пермца) • Известно с 1478 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Древнейшее село юга Коми земли на правом берегу реки Лузы, впервые упомянутое в летописях в 1478 году (близ села исследован Лоемский могильник IX–X веков). Село славится уникальным архаичным лоемским говором и величественным каменным храмом Успения Пресвятой Богородицы (построен в 1802–1804 гг.) с росписями Васнецовской школы 1916 г. <strong>Родина Марии Степановны Сюткиной (Шехониной) (1911–1981)</strong>, её сестры Александры (род. 1922), их отца Степана Петровича Сюткина (1880–1933, раскулаченного в 1930 г.) и деда Петра Сюткина.</p>
        </div>

        <!-- ЕРОЗДИНО -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#d97706; margin-bottom:0.35rem;">🌲 Деревня Ероздино (Йӧрӧсдін)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Ыбский куст / Вымь • Известна с 1602 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Старинная коми деревня, название которой происходит от коми слов <em>«йӧрӧс»</em> (речной порог, быстрина) и <em>«дін»</em> (около, устье) — «селение у речного порога». Историческая родина предков <strong>Шуктомовых, Полещиковых и Поздеевых</strong>. Здесь родились прадед Евгений Александрович Шуктомов (род. 1946), прапрадед Александр Михайлович Шуктомов (род. 1911), прапрабабушка Серафима Афанасьевна Полещикова (род. 1912). Из Ероздино также происходит выдающийся коми филолог и писатель Адольф Иванович Туркин (1936–1996).</p>
        </div>

        <!-- ВОГВАЗДИНО -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#059669; margin-bottom:0.35rem;">⛵ Деревня Вогваздино / Вагваздино (Ванвисдін)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Усть-Вымский район • Слияние Выми и Вычегды • Известна с 1678 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Селение при впадении реки Вымь в Вычегду — колыбель зырянского православия святителя Стефана Пермского. В XVII веке фиксировалось как починок Боровой (местные жители называли «Яг» — сосновый бор). Коми название расшифровывается как <em>«вок Вась дін»</em> — «место у брата Василия». Родина прапрапрапрабабушки <strong>Параскевы Ивановны Кругляковой (Пасынковой)</strong> (род. 1828) и старейшей известной представительницы 9-го поколения <strong>Марии Григорьевны Кругляковой</strong>.</p>
        </div>

        <!-- ЛЯЛИ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#ec4899; margin-bottom:0.35rem;">🏰 Деревня Ляли (Ляй)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Княжпогостский район • Река Вымь • Погост с 1608 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Древний погост на левом берегу реки Вымь, старинном Вымском речном торговом пути в Сибирь. Название восходит к финно-угорскому <em>«ляй»</em> (ручей в овраге, ключевая речка). В 1856 году здесь был воздвигнут каменный Богоявленский храм. Родина коми родов <strong>Каракчиевых</strong> (Анастасия Андреевна Каракчиева, род. 1851) и <strong>Шилиных</strong> (Александра Николаевна Шилина, род. 1839).</p>
        </div>

        <!-- ПАЛЬТЫДОР -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#2563eb; margin-bottom:0.35rem;">🏡 Деревня Пальтыдор (Калтыдор)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Сысольский / Усть-Вымский уезд • Основана в 1707–1719 гг.</div>
          <p style="font-size:0.86rem; line-height:1.5;">Основана в начале XVIII века в ходе крестьянского освоения новых пашен. Компонент <em>«дор»</em> на коми языке означает «край, берег, селение у воды/леса». Родина прапрабабушки <strong>Павлы Савватеевны Летовой (Туркиной)</strong> (род. 09.08.1908) и её матери <strong>Александры Семеновны Летовой (Ярановой)</strong> (род. 04.05.1874).</p>
        </div>

                <!-- КОКВИЦЫ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#2563eb; margin-bottom:0.35rem;">⛰️ Село Коквицы (Коквицкая гора)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Усть-Вымский район • Левый берег Вычегды (Эжвы) • Известно с 1483 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Знаменитая Коквицкая гора — возвышенность-«полуостров», омываемая Вычегдой, колыбель вычегодских коми (эжватас). Одно из легендарных сакральных мест Коми края со святынями времен Стефана Пермского. <strong>Главный духовный оплот рода Туркиных:</strong> при каменной Христорождественской церкви более 150 лет служили священники о. Степан и о. Иван, диакон о. Алексей, пономари Леонтий и Елисей. Родина прадеда Аркадия Михайловича (1935) и прапрадеда Михаила Николаевича (1906).</p>
        </div>

        <!-- ОКВАД -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#0284c7; margin-bottom:0.35rem;">⛪ Погост Оквад (Катвад)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Оквадская волость • Берег Вычегды • Погост с XVI века</div>
          <p style="font-size:0.86rem; line-height:1.5;">Древнейшая задокументированная родина Туркиных. В писцовой книге 1608 г. здесь жил молодой домохозяин Микитка Туркин, а в переписной книге 1646 г. — архиепископский приказной человек Афанасий Семёнович Туркин с 11-летним сыном Исааком. При местной церкви Введения Пресвятой Богородицы служили церковный дьячок Исаакий Афанасьевич (1678 г.) и священник о. Автоном Лаврентьевич (1731–1736 гг.).</p>
        </div>

        <!-- УСТЬ-ВЫМЬ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#059669; margin-bottom:0.35rem;">🏛️ Село Усть-Вымь (Емдін)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Слияние Выми и Вычегды • Основано св. Стефаном Пермским в 1380 г.</div>
          <p style="font-size:0.86rem; line-height:1.5;">Исторический, административный и кафедральный центр Пермской епархии. В Благовещенской церкви Усть-Выми служил священник о. Пётр Исаакович Туркин (прямой 8-й прадед Николая, зафиксирован в метрической книге 1731 года, ГААО). Волостной центр, к которому в XIX веке относились государственные крестьяне Туркины (8-я ревизия 1834 г., ГАВО).</p>
        </div>

        <!-- СЮЛАТУЙСКАЯ -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#2563eb; margin-bottom:0.35rem;">🌲 Деревня Сюлатуйская (Сюлатуй)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Усть-Сысольский уезд • Ыбская волость</div>
          <p style="font-size:0.86rem; line-height:1.5;">Название деревни на коми языке означает: <em>«сюла»</em> (смолистый, кедровый ключ) + <em>«туй»</em> (тропа, дорога) — «путь к смолистому источнику». <strong>Место рождения прапрадеда Николая Алексеевича Туркина</strong> (03.11.1876 г., зафиксировано в метрической книге, ссылка в семейном архиве «с. 267»).</p>
        </div>

        <!-- СЫКТЫВКАР -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#0284c7; margin-bottom:0.35rem;">🏙️ Город Сыктывкар (до 1930 г. — Усть-Сысольск)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Столица Республики Коми • Слияние Сысолы и Вычегды • Город с 1780 года</div>
          <p style="font-size:0.86rem; line-height:1.5;">Главный административный, промышленный и культурный центр Коми края. На коми языке: <em>«Сыктыв»</em> (река Сысола) + <em>«кар»</em> (город) — «город на Сысоле». Родина нескольких поколений семьи XX века: дедушки Михаила Аркадьевича Туркина (род. 1970), бабушки Светланы Евгеньевны Туркиной (род. 1970), отца Вячеслава Михайловича (род. 1991) и дяди Никиты Михайловича (род. 2000).</p>
        </div>

        <!-- УЛЬЯНОВО И КУЖБА -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#4f46e5; margin-bottom:0.35rem;">🌲 Село Ульяново и село Кужба</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Усть-Куломский район • Верхняя Вычегда • Основаны в XIV–XVII вв.</div>
          <p style="font-size:0.86rem; line-height:1.5;">Священные места Верхней Вычегды. В Ульяново расположен Троице-Стефановский мужской монастырь, основанный святителем Стефаном Пермским в 1385 году. Обитель монашеского служения <strong>монаха Виталия (Виталия Ивановича Туркина) (1865–1937)</strong>. В соседнем селе Кужба после закрытия обители он совершал требы на дому вместе со священномучеником иеромонахом Мелетием (Федюнёвым).</p>
        </div>

        <!-- ЧУМПХОН -->
        <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="font-weight:700; font-size:1.05rem; color:#10b981; margin-bottom:0.35rem;">🌴 Город Чумпхон (ชุมพร / Chumphon)</div>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem;">Королевство Таиланд • Побережье Сиамского залива • Перешеек Кра</div>
          <p style="font-size:0.86rem; line-height:1.5;">Древний приморский город и провинция на юге Таиланда, исторически известный как «Ворота Южного Таиланда» (Gateway to the South). В средние века город служил важным военным форпостом защиты столицы Сиама Аюттхаи (название связывают с «Chumnumphon» — место благословения и сбора рати). <strong>Место рождения пробанда рода Николая Вячеславовича Туркина</strong> (2024 г.).</p>
        </div>
      </div>
    </div>

    <!-- ONOMASTICS AND SURNAMES SECTION -->
    <div class="info-card" id="info-surnames">
      <h2>🧬 Происхождение фамилий и история родов</h2>
      <p style="color:var(--text-muted); margin-bottom:1.25rem;">Ономастическое исследование коми и тайских родовых имен, вошедших в родословную:</p>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1rem;">
        <!-- ТУРКИНЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#2563eb; font-size:0.98rem;">Туркины</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#eff6ff; color:#2563eb; border-radius:4px; font-weight:700;">Поколения I – XVI (с 1608 г., истоки с 1490 г.)</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Коренной северный род священнослужителей, монашествующих и крестьян Яренского уезда (Оквад, Коквицы). Древнейшие первоисточники: <strong>Дозорная книга 1608 г.</strong> с молодым домохозяином Микиткой Туркиным и родоначальником прямой мужской линии Семёном Туркиным; <strong>Переписная книга 1646 г.</strong> (РГАДА, ф. 1209, д. 1080) с двором архиепископского приказного человека Афанасия Семёнова сына Туркина с 11-летним сыном Исааком. Прямая мужская линия непрерывно соединяет 15 поколений до Николая Вячеславовича (2024 г.).</p>
        </div>

        <!-- ЛЕТОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#2563eb; font-size:0.98rem;">Летовы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#eff6ff; color:#2563eb; border-radius:4px; font-weight:700;">д. Пальтыдор (с 1650 г.)</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Старинный род деревни Палтыдор Коквицкой волости. 2-я ревизия 1748 г. (РГАДА, ф. 350, д. 4216) зафиксировала родоначальников: Кирило Харитонов Летов (70 лет, род. ~1678, дед Харитон род. ~1650 г.), Василий Степанов Летов (45 лет, род. ~1703). В роду: Павла Савватеевна (Летова) Туркина (род. 1908), её отец Савватий Васильевич Летов.</p>
        </div>

        <!-- ЯРАНОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#2563eb; font-size:0.98rem;">Ярановы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#eff6ff; color:#2563eb; border-radius:4px; font-weight:700;">Поколения VI – VII</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Фамилия имеет глубокое этнографическое значение: на коми языке слово <em>«яран»</em> означает ненца, оленевода или человека, пришедшего из тундровых промыслов. В роду: Александра Семеновна (Яранова) Летова (род. 1874) и её отец Симеон Васильевич Яранов.</p>
        </div>

        <!-- СИЗЕВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#2563eb; font-size:0.98rem;">Сизевы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#eff6ff; color:#2563eb; border-radius:4px; font-weight:700;">Поколения VI – VII</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Чисто зырянская по происхождению фамилия, восходящая к коми дохристианскому имени <em>«Сизь»</em> — дятел (птица-символ трудолюбия, упорства и лесного мастерства). В роду: Павла Ивановна (Сизева) Туркина (род. 1883) и её отец Иван Семенович Сизев.</p>
        </div>

        <!-- СЮТКИНЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#8b5cf6; font-size:0.98rem;">Сюткины</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#f5f3ff; color:#8b5cf6; border-radius:4px; font-weight:700;">с. Лойма</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Фамилия характерна для бассейна реки Лузы (Прилузье). Образована от северной уменьшительно-ласкательной формы <em>Сютко</em> от христианского имени Евсей / Евсевий либо Исихий / Сюня. В роду: Мария Степановна (Сюткина) Шехонина (1911–1981), её отец Степан Петрович Сюткин (1880–1933) и дед Пётр Сюткин; а также Анна Андреевна (Сюткина) Шехонина и её отец Андрей Александрович Сюткин.</p>
        </div>

        <!-- ШЕХОНИНЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#8b5cf6; font-size:0.98rem;">Шехонины</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#f5f3ff; color:#8b5cf6; border-radius:4px; font-weight:700;">Поколения IV – VII</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Старинная северная фамилия, происходящая от прозвища <em>Шехоня</em> (выходец с реки Шексны либо живой, расторопный человек). В роду: Зинаида Михайловна (Шехонина) Туркина (род. 1940), Михаил Афанасьевич Шехонин (1909–1988), Афанасий Давидович Шехонин и Давид Шехонин.</p>
        </div>

        <!-- ШУКТОМОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#d97706; font-size:0.98rem;">Шуктомовы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fffbeb; color:#d97706; border-radius:4px; font-weight:700;">д. Ероздино</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Древнейший коренной коми род. Фамилия происходит от коми слова <em>«шуктом»</em> — прямой, гладкий ствол дерева без сучьев (символ честности и статности). В роду: Светлана Евгеньевна (Шуктомова) Туркина (род. 1970), Евгений Александрович (род. 1946), Александр Михайлович (род. 1911), Михаил Иванович Шуктомов.</p>
        </div>

        <!-- ПОЛЕЩИКОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#d97706; font-size:0.98rem;">Полещиковы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fffbeb; color:#d97706; border-radius:4px; font-weight:700;">д. Ероздино</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Фамилия происходит от профессионального звания <em>«полесовщик» / «полещик»</em> — государственный лесной смотритель, егерь на Вычегде и Сысоле. В роду: Серафима Афанасьевна (Полещикова) Шуктомова (род. 1912), Афанасий Галактионович (род. 1886), Галактион Афанасьевич Полещиков.</p>
        </div>

        <!-- ПАСЫНКОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#d97706; font-size:0.98rem;">Пасынковы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fffbeb; color:#d97706; border-radius:4px; font-weight:700;">с. Ыб • с 1827 г.</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Известнейший крестьянский и духовный коми род Ыбской волости. В роду: Мария Платоновна (Пасынкова) Шуктомова (род. 1877), Платон Харлампиевич Пасынков (род. 1851, венчание 10.11.1874), Харлампий Яковлевич Пасынков (род. 1827, венчание 24.04.1846 в 19 лет).</p>
        </div>

        <!-- КРУГЛЯКОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#d97706; font-size:0.98rem;">Кругляковы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fffbeb; color:#d97706; border-radius:4px; font-weight:700;">Поколения VIII – IX</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">От мирского имени Кругляк (крепкий, плотный, здоровый человек). В роду: Параскева Ивановна (Круглякова) Пасынкова (род. 1828 в д. Вагваздино, венчалась в 18 лет в 1846 г.) и старейшая женщина родословной Мария Григорьевна Круглякова (род. нач. XIX века).</p>
        </div>

        <!-- ЗИНОВЬЕВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#ec4899; font-size:0.98rem;">Зиновьевы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fff1f2; color:#ec4899; border-radius:4px; font-weight:700;">с. Ыб • с 1890 г.</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">От крестильного греческого имени Зиновий («живущий по воле Зевса/Бога»). В роду: прабабушка Альбина Семеновна (Зиновьева) Гладышева (род. 1946), Семен Григорьевич Зиновьев (род. 27.01.1890 в с. Ыб), Григорий Иванович Зиновьев.</p>
        </div>

        <!-- ПОЗДЕЕВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#ec4899; font-size:0.98rem;">Поздеевы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fff1f2; color:#ec4899; border-radius:4px; font-weight:700;">д. Ероздино</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Древнейшее славяно-северное охранительное имя <em>Поздей</em> («поздний, желанный сын»). В роду: Мария Ивановна (Поздеева) Зиновьева (род. 1860 в д. Ероздино), Иван Иванович Поздеев (род. 1835, венчание 24.01.1858 в возрасте 23 лет).</p>
        </div>

        <!-- КЫЗЪЮРОВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#ec4899; font-size:0.98rem;">Кызъюровы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fff1f2; color:#ec4899; border-radius:4px; font-weight:700;">с. Малый Ыб</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Уникальная чисто зырянская фамилия: от коми <em>«кыз»</em> (ель) + <em>«юр»</em> (вершина, голова, мыс) — «вершина ели». В роду: Клавдия Ильинична (Кызъюрова) Зиновьева (род. 1900), Илья Иванович Кызъюров (род. 30.06.1865 в Мелком Ыбе), Иван Григорьевич Кызъюров (род. 1836, венчание 18.01.1859 в 23 года).</p>
        </div>

        <!-- АЙБАБИНЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#ec4899; font-size:0.98rem;">Айбабины</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fff1f2; color:#ec4899; border-radius:4px; font-weight:700;">Поколения VI – VII</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Редкая коми фамилия Сысольской земли. В роду: Елисавета Петровна (Айбабина) Кызъюрова (род. 1867) и её отец Пётр Борисович Айбабин.</p>
        </div>

        <!-- КАРАКЧИЕВЫ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#ec4899; font-size:0.98rem;">Каракчиевы</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#fff1f2; color:#ec4899; border-radius:4px; font-weight:700;">д. Ляли • на Выми</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Древний вымский род (страж, дозорный речной заставы). В роду: Анастасия Андреевна (Каракчиева) Пасынкова (род. 1851 в д. Ляли), Синклитикия Ионична (Каракчиева) Поздеева (род. 1841, венчание 24.01.1858 в 17 лет), Иона Агафонович Каракчиев (род. ок. 1820 г.).</p>
        </div>

        <!-- ПИТАК -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#10b981; font-size:0.98rem;">Питак (Pithak, พิทักษ์)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#ecfdf5; color:#10b981; border-radius:4px; font-weight:700;">Таиланд</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Тайская благородная фамилия санскритского корня, означающая <em>«Хранитель, Защитник, Оберегающий покровитель»</em> (в Таиланде ассоциируется с верностью долгу и защитой семейного очага). В роду: мать Парита Питак (род. 1997), тетя Наримон Питак (род. 1993), дядя Нарет Питак (род. 1986), дедушка Пхуан Питак.</p>
        </div>

        <!-- ПАМАЙТОНГ -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#10b981; font-size:0.98rem;">Памайтонг (Pamaitong, ป่าไม้ทอง)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#ecfdf5; color:#10b981; border-radius:4px; font-weight:700;">Таиланд</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Поэтичная тайская фамилия, состоящая из слов <em>«памай»</em> (ป่าไม้ — лес, роща) и <em>«тонг»</em> (ทอง — золото). Буквально означает <em>«Золотой лес / Золотая роща»</em> — символ природного плодородия и благословения. В роду: бабушка Дуангдюан Памайтонг (род. 1961), прабабушка Сай Памайтонг (род. 1919), прадедушка Пуанг Памайтонг, дядя Тхавач Памайтонг (род. 1979).</p>
        </div>

        <!-- ЧАМНИАНКАН -->
        <div style="background:var(--bg-primary); padding:0.9rem 1rem; border-radius:8px; border:1px solid var(--border-color);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <strong style="color:#10b981; font-size:0.98rem;">Чамнианкан (Chamniankan, ชำนาญการ)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.4rem; background:#ecfdf5; color:#10b981; border-radius:4px; font-weight:700;">Таиланд</span>
          </div>
          <p style="font-size:0.84rem; line-height:1.45;">Тайская фамилия, означающая <em>«Искусный знаток, Мастер своего дела, Профессионал высокого ранга»</em>. В роду представлена тётей Николая Нонгнут Чамнианкан (род. 1981).</p>
        </div>
      </div>
    </div>

    <!-- BOTTOM ANCHOR NAVIGATION BAR FOR PLACES & ROOTS -->
    <nav class="info-bottom-bar" id="infoBottomBar">
      <div class="info-bottom-scroll">
        <a href="#info-overview" class="info-bottom-pill active" onclick="scrollToAnchor(event, 'info-overview')">
          <span>🌳</span> <span class="pill-lbl-full">О семье</span><span class="pill-lbl-short">Семья</span>
        </a>
        <a href="#info-heroes" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-heroes')">
          <span>🎖️</span> <span class="pill-lbl-full">Защитники</span><span class="pill-lbl-short">Герои</span>
        </a>
        <a href="#info-clergy" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-clergy')">
          <span>⛪</span> <span class="pill-lbl-full">Духовенство</span><span class="pill-lbl-short">Храмы</span>
        </a>
        <a href="#info-geography" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-geography')">
          <span>🗺️</span> <span class="pill-lbl-full">География</span><span class="pill-lbl-short">Места</span>
        </a>
        <a href="#info-surnames" class="info-bottom-pill" onclick="scrollToAnchor(event, 'info-surnames')">
          <span>🧬</span> <span class="pill-lbl-full">Фамилии</span><span class="pill-lbl-short">Роды</span>
        </a>
      </div>
    </nav>
  </div>

  <!-- TAB 6: SOURCES AND BIBLIOGRAPHY VIEW -->
  <div id="view-sources" class="view-section">

    <!-- MAIN HERO SOURCES CARD -->
    <div class="info-card" style="background: linear-gradient(135deg, rgba(37,99,235,0.07), rgba(217,119,6,0.07)); border: 1.5px solid var(--border-color); margin-bottom:1.5rem;">
      <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.6rem;">
        <span style="font-size:2.2rem;">📚</span>
        <div>
          <h2 style="margin:0; font-size:1.35rem; color:var(--text-main);">Источники генеалогического исследования</h2>
          <div style="font-size:0.84rem; color:var(--text-muted); margin-top:0.2rem;">Сводный научный каталог первоисточников: летописи XV–XVII вв., государственные архивы Москвы, Вологды и Сыктывкара, базы данных Великой Отечественной войны и фундаментальные издания серии «Усть-Вымское родословие»</div>
        </div>
      </div>
      <p style="font-size:0.92rem; line-height:1.65; color:var(--text-main); margin-bottom:0.75rem;">
        Генеалогическое исследование рода Туркиных и родственных фамилий выстроено на непрерывной документальной доказательной базе с 1490 по 2026 год (свыше 530 лет истории, 20 поколений). Исследование объединяет материалы пяти государственных архивов (РГАДА, ГАВО, ВЦА, НАРК, ЦАМО), древнерусские летописи и актовые публикации, базы данных духовенства и фундаментальные труды исследователей-краеведов.
      </p>
      <div style="display:flex; gap:0.6rem; flex-wrap:wrap; margin-top:0.85rem;">
        <button class="pill-btn" onclick="switchTab('archive')" style="font-size:0.82rem; padding:0.45rem 0.9rem; background:var(--accent); color:#fff; border:none; cursor:pointer; font-weight:600; box-shadow:0 2px 5px rgba(37,99,235,0.25);">🏛️ Архив первоисточников древа ({len(archive_catalog.DOCS_CATALOG)} документов)</button>
        <a href="#books-series" class="pill-btn" style="font-size:0.82rem; padding:0.45rem 0.85rem; text-decoration:none; color:var(--text-main); background:var(--bg-primary); border:1px solid var(--border-color); font-weight:600;">📖 Книги «Усть-Вымское родословие»</a>
        <a href="#ancient-chronicles" class="pill-btn" style="font-size:0.82rem; padding:0.45rem 0.85rem; text-decoration:none; color:var(--text-main); background:var(--bg-primary); border:1px solid var(--border-color); font-weight:600;">📜 Летописи и грамоты XV–XVII вв.</a>
        <a href="#state-archives" class="pill-btn" style="font-size:0.82rem; padding:0.45rem 0.85rem; text-decoration:none; color:var(--text-main); background:var(--bg-primary); border:1px solid var(--border-color); font-weight:600;">🏛️ РГАДА, ГАВО и НАРК</a>
        <a href="#ww2-archives" class="pill-btn" style="font-size:0.82rem; padding:0.45rem 0.85rem; text-decoration:none; color:var(--text-main); background:var(--bg-primary); border:1px solid var(--border-color); font-weight:600;">🎖️ Военные архивы ЦАМО</a>
        <a href="#online-databases" class="pill-btn" style="font-size:0.82rem; padding:0.45rem 0.85rem; text-decoration:none; color:var(--text-main); background:var(--bg-primary); border:1px solid var(--border-color); font-weight:600;">🌐 Научные базы и публикации</a>
      </div>
    </div>

    <!-- 1. BOOKS SERIES: UST-VYM GENEALOGY -->
    <div id="books-series" class="info-card" style="margin-bottom:1.5rem; border-left: 4px solid #2563eb;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <div>
          <h3 style="margin:0; font-size:1.22rem; color:#2563eb;">📖 Фундаментальные краеведческие издания: Серия «Усть-Вымское родословие»</h3>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.15rem;">Научная и генеалогическая основа восстановления семейных линий Вычегодского края с XVIII по XXI век</div>
        </div>
        <span style="font-size:0.75rem; background:#eff6ff; color:#2563eb; font-weight:700; padding:0.25rem 0.65rem; border-radius:20px; border:1px solid #bfdbfe;">3 тома серии</span>
      </div>
      <p style="font-size:0.9rem; line-height:1.65; color:var(--text-main); margin-bottom:0.75rem;">
        При подготовке рукописной основы родословной (66 персон, 9 поколений с конца XVIII по XXI век) ключевую роль сыграли труды замечательных родоведов-краеведов Усть-Вымского района. Семья выражает глубокую признательность и искреннюю благодарность <strong>Лидии Афанасьевне Молодцовой</strong>, <strong>Валентине Александровне Гусевой</strong> и <strong>Людмиле Владимировне Ванеевой</strong>, историко-генеалогическому клубу <strong>«Емдiнса родовед» («Родовед»)</strong>, <strong>Усть-Вымскому землячеству Республики Коми</strong>, Администрации МР «Усть-Вымский» и Национальной библиотеке Республики Коми за подвижнический труд по сохранению исторической памяти северных коми родов.
      </p>

      <!-- THREE MAIN BOOKS GRID -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem; margin-top:1.25rem; margin-bottom:1.25rem;">
        
        <!-- VOLUME 1 - MOLODTSOVA -->
        <div style="background:var(--bg-surface); border-radius:12px; border:1.5px solid rgba(37,99,235,0.3); padding:1.25rem; box-shadow:var(--shadow); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
              <div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap; margin-bottom:0.35rem;">
                  <span style="background:#eff6ff; color:#2563eb; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #bfdbfe;">Том 1 серии</span>
                  <span style="background:var(--bg-primary); border:1px solid var(--border-color); font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:6px; font-weight:600;">2020 г.</span>
                </div>
                <h3 style="margin:0; font-size:1.15rem; color:#2563eb;">«Усть-Вымское родословие. Коквицкая „гора“»</h3>
                <div style="font-size:0.92rem; font-weight:600; color:var(--text-main); margin-top:0.25rem;">Автор: Лидия Афанасьевна Молодцова</div>
              </div>
            </div>

            <div style="display:flex; gap:1rem; margin-bottom:1rem; align-items:flex-start;">
              <a href="книги_родословия/Усть-Вымское_родословие_Том1_Молодцова_обложка.jpg" target="_blank" title="Нажмите, чтобы открыть обложку в полном размере">
                <img src="книги_родословия/Усть-Вымское_родословие_Том1_Молодцова_обложка.jpg" alt="Обложка тома 1 Молодцовой" style="width:115px; height:165px; object-fit:cover; border-radius:8px; border:1.5px solid rgba(37,99,235,0.4); box-shadow:0 4px 10px rgba(0,0,0,0.15); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">
                <div>📘 <strong>Голубой переплёт</strong> с золотым тиснением и эмблемой древа жизни.</div>
                <div style="margin-top:0.45rem;">🏛️ Издано при поддержке Администрации МР «Усть-Вымский» и Усть-Вымского землячества.</div>
                <div style="margin-top:0.45rem;">📍 Приходы Коквицкой Христорождественской и Лыатинской церквей.</div>
              </div>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; color:var(--text-main);">
              <div style="margin-bottom:0.45rem;">
                <strong>Географический охват:</strong> селения <strong>Коквицкой горы</strong> (Коквицы, Сюлатуй, Пальтыдор, Семуково и др.).
              </div>
              <div>
                <strong>Значение для родословной:</strong>
                <ul style="margin:0.25rem 0 0 1.1rem; padding:0;">
                  <li><strong>Село Коквицы и д. Сюлатуйская:</strong> прямая мужская линия <strong>Туркиных</strong> (Николай Алексеевич, Михаил Николаевич, Аркадий Михайлович);</li>
                  <li><strong>Деревня Пальтыдор:</strong> предки <strong>Летовы и Ярановы</strong> (Павла Савватеевна Летова, Александра Семеновна Яранова);</li>
                  <li>Детальная расшифровка ревизий XVIII–XIX веков.</li>
                </ul>
              </div>
            </div>
          </div>

          <div style="margin-top:1rem; padding-top:0.75rem; border-top:1px dashed var(--border-color); display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.78rem; color:var(--text-muted);">Ветви: Туркины • Летовы • Ярановы • Сизевы</span>
            <a href="книги_родословия/Усть-Вымское_родословие_Том1_Молодцова_обложка.jpg" target="_blank" class="pill-btn" style="font-size:0.75rem;">🔍 Обложка тома 1</a>
          </div>
        </div>

        <!-- VOLUME 2 - GUSEVA -->
        <div style="background:var(--bg-surface); border-radius:12px; border:1.5px solid rgba(159,18,57,0.3); padding:1.25rem; box-shadow:var(--shadow); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
              <div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap; margin-bottom:0.35rem;">
                  <span style="background:#ffe4e6; color:#9f1239; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fecdd3;">Том 2 серии</span>
                  <span style="background:var(--bg-primary); border:1px solid var(--border-color); font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:6px; font-weight:600;">2022 г.</span>
                </div>
                <h3 style="margin:0; font-size:1.15rem; color:#9f1239;">«Усть-Вымское родословие» (Том 2)</h3>
                <div style="font-size:0.92rem; font-weight:600; color:var(--text-main); margin-top:0.25rem;">Автор: Валентина Александровна Гусева</div>
              </div>
            </div>

            <div style="display:flex; gap:1rem; margin-bottom:1rem; align-items:flex-start;">
              <a href="книги_родословия/Усть-Вымское_родословие_Том2_Гусева_обложка.jpg" target="_blank" title="Нажмите, чтобы открыть обложку в полном размере">
                <img src="книги_родословия/Усть-Вымское_родословие_Том2_Гусева_обложка.jpg" alt="Обложка тома 2 Гусевой" style="width:115px; height:165px; object-fit:cover; border-radius:8px; border:1.5px solid rgba(159,18,57,0.4); box-shadow:0 4px 10px rgba(0,0,0,0.15); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">
                <div>📕 <strong>Бордовый переплёт</strong> с золотым тиснением и символом древа жизни.</div>
                <div style="margin-top:0.45rem;">🏛️ Выпущен при содействии Усть-Вымского землячества. Автор удостоена награды Госсовета Республики Коми.</div>
                <div style="margin-top:0.45rem;">📍 Приходы Усть-Вымского церковного округа.</div>
              </div>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; color:var(--text-main);">
              <div style="margin-bottom:0.45rem;">
                <strong>Географический охват:</strong> селения и волости бассейна Вычегды и Выми, приходы Усть-Вымского края.
              </div>
              <div>
                <strong>Значение для родословной:</strong>
                <ul style="margin:0.25rem 0 0 1.1rem; padding:0;">
                  <li>Связующее звено между Коквицким кустом (Том 1) и селениями Вычегодского поречья (Том 3);</li>
                  <li>Детальная роспись семейных связей и брачных союзов соседних волостей;</li>
                  <li>Документальное подтверждение миграционных путей семей коми крестьян.</li>
                </ul>
              </div>
            </div>
          </div>

          <div style="margin-top:1rem; padding-top:0.75rem; border-top:1px dashed var(--border-color); display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.78rem; color:var(--text-muted);">Приходы Вычегды и Выми • Родовые связи</span>
            <a href="книги_родословия/Усть-Вымское_родословие_Том2_Гусева_обложка.jpg" target="_blank" class="pill-btn" style="font-size:0.75rem;">🔍 Обложка тома 2</a>
          </div>
        </div>

        <!-- VOLUME 3 - VANEEVA -->
        <div style="background:var(--bg-surface); border-radius:12px; border:1.5px solid rgba(217,119,6,0.3); padding:1.25rem; box-shadow:var(--shadow); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
              <div>
                <div style="display:flex; gap:0.4rem; flex-wrap:wrap; margin-bottom:0.35rem;">
                  <span style="background:#fef3c7; color:#b45309; font-weight:700; font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:6px; border:1px solid #fde68a;">Том 3 серии</span>
                  <span style="background:var(--bg-primary); border:1px solid var(--border-color); font-size:0.75rem; padding:0.2rem 0.5rem; border-radius:6px; font-weight:600;">Март 2026 г.</span>
                </div>
                <h3 style="margin:0; font-size:1.15rem; color:#b45309;">«Усть-Вымское родословие» (Том 3)</h3>
                <div style="font-size:0.92rem; font-weight:600; color:var(--text-main); margin-top:0.25rem;">Автор: Людмила Владимировна Ванеева</div>
              </div>
            </div>

            <div style="display:flex; gap:1rem; margin-bottom:1rem; align-items:flex-start;">
              <a href="книги_родословия/Усть-Вымское_родословие_Том3_Ванеева_обложка.jpg" target="_blank" title="Нажмите, чтобы открыть обложку в полном размере">
                <img src="книги_родословия/Усть-Вымское_родословие_Том3_Ванеева_обложка.jpg" alt="Обложка тома 3 Ванеевой" style="width:115px; height:165px; object-fit:cover; border-radius:8px; border:1.5px solid rgba(217,119,6,0.4); box-shadow:0 4px 10px rgba(0,0,0,0.15); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
              </a>
              <div style="font-size:0.82rem; color:var(--text-muted); line-height:1.5;">
                <div>📘 <strong>Синий переплёт</strong> с традиционным орнаментом коми пасов.</div>
                <div style="margin-top:0.45rem;">🏛️ Вышел в свет в марте 2026 года в Сыктывкаре, презентован в Национальной библиотеке РК.</div>
                <div style="margin-top:0.45rem;">📍 Приходы Часовской, Айкинской и Усть-Вымской волостей.</div>
              </div>
            </div>

            <div style="font-size:0.85rem; line-height:1.55; color:var(--text-main);">
              <div style="margin-bottom:0.45rem;">
                <strong>Географический охват:</strong> селения по реке Вычегде (Ероздино, Часово, Горелый Ыб, Ляли и др.).
              </div>
              <div>
                <strong>Значение для родословной:</strong>
                <ul style="margin:0.25rem 0 0 1.1rem; padding:0;">
                  <li><strong>Деревня Ероздино (Йӧрӧсдін):</strong> предки <strong>Шуктомовы, Полещиковы и Поздеевы</strong> (Евгений Александрович, Серафима Афанасьевна);</li>
                  <li><strong>Деревня Горелый Ыб (с. Горесоит):</strong> предки <strong>Зиновьевы и Кызъюровы</strong> (герой войны Владимир Семенович Зиновьев);</li>
                  <li>Точнейшая привязка к метрикам и ревизским сказкам XIX века.</li>
                </ul>
              </div>
            </div>
          </div>

          <div style="margin-top:1rem; padding-top:0.75rem; border-top:1px dashed var(--border-color); display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:0.78rem; color:var(--text-muted);">Ветви: Шуктомовы • Зиновьевы • Поздеевы • Кызъюровы</span>
            <a href="книги_родословия/Усть-Вымское_родословие_Том3_Ванеева_обложка.jpg" target="_blank" class="pill-btn" style="font-size:0.75rem;">🔍 Обложка тома 3</a>
          </div>
        </div>

      </div>

      <!-- PARTNERS AND COMMUNITY CARD -->
      <div style="background:var(--bg-primary); padding:1rem; border-radius:8px; border:1px solid var(--border-color); margin-top:1rem;">
        <h4 style="margin:0 0 0.5rem 0; font-size:0.98rem; color:var(--text-main);">🤝 Исследовательские организации и соавторы издательского проекта:</h4>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:0.75rem; font-size:0.84rem; line-height:1.5;">
          <div>🏛️ <strong>Клуб «Емдiнса родовед» («Родовед»)</strong>: действует при Усть-Вымском землячестве более 10 лет под руководством генеалога-исследователя <strong>Анатолия Алексеевича Гобанова</strong>.</div>
          <div>🌲 <strong>Усть-Вымское землячество Республики Коми</strong>: председатель <strong>Валерьян Николаевич Исаков</strong>, организатор подготовки книг <strong>Лидия Константиновна Дубленникова</strong>.</div>
          <div>📚 <strong>Национальная библиотека Республики Коми</strong>, Усть-Вымская МБС и районная газета <strong>«Вперёд»</strong>, бережно освещающие выход родословий края.</div>
        </div>
      </div>
    </div>

    <!-- 2. ANCIENT CHRONICLES AND CHARTERS (XV–XVII BB.) -->
    <div id="ancient-chronicles" class="info-card" style="margin-bottom:1.5rem; border-left: 4px solid #b91c1c;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <div>
          <h3 style="margin:0; font-size:1.22rem; color:#b91c1c;">📜 Древнерусские летописи и актовые первоисточники (XV–XVII вв.)</h3>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.15rem;">Древнейшие письменные памятники Московского государства с упоминанием родоначальников Туркиных</div>
        </div>
        <span style="font-size:0.75rem; background:#fef2f2; color:#b91c1c; font-weight:700; padding:0.25rem 0.65rem; border-radius:20px; border:1px solid #fecaca;">XV–XVII века</span>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem;">
        
        <!-- 1490 IVAN III CHARTER -->
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <span style="background:#fee2e2; color:#991b1b; font-size:0.75rem; font-weight:700; padding:0.15rem 0.5rem; border-radius:4px;">1490 год (6998 г.)</span>
              <span style="font-size:0.75rem; color:var(--text-muted);">Царствование Ивана III</span>
            </div>
            <h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; color:var(--text-main);">Жалованная грамота великого князя Ивана III епископу Филофею</h4>
            <p style="font-size:0.85rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              Древнейший актовый документ рода. В перечне деревень погоста Аквад (Оквад) при церкви Введения Богородицы зафиксирован прародитель патронима: <em>«вд. Митинской Мышева Турка малой да Митка Степанов Чирак... сины дети»</em>.
            </p>
            <div style="font-size:0.8rem; color:var(--text-muted); line-height:1.45; margin-bottom:0.75rem;">
              <strong>Публикация:</strong> Вычегодско-Вымская (Мисаило-Евтихиевская) летопись / подгот. П. Г. Доронин, 1958. Список сохранён крестьянином Иваном Туркиным (Лудником).
            </div>
          </div>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap; padding-top:0.65rem; border-top:1px dashed var(--border-color);">
            <a href="https://www.vostlit.info/Texts/Dokumenty/Russ/XII/1160-1180/Vycegod_vymsk_let/text1.phtml" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#b91c1c; font-weight:600; background:#fff1f2; border:1px solid #fecaca;">🌐 Читать на «Восточной Литературе» (№ 3) ↗</a>
            <button onclick="openDocViewerById('ancient_1490_ivan3_turka')" class="pill-btn" style="font-size:0.76rem; background:var(--bg-primary); border:1px solid var(--border-color); cursor:pointer;">🔍 Карточка в архиве</button>
          </div>
        </div>

        <!-- 1608 CADASTRE SHUYSKY -->
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
              <span style="background:#e0f2fe; color:#0369a1; font-size:0.75rem; font-weight:700; padding:0.15rem 0.5rem; border-radius:4px;">1608 год (7116 г.)</span>
              <span style="font-size:0.75rem; color:var(--text-muted);">Царь Василий Шуйский</span>
            </div>
            <h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; color:var(--text-main);">Писцовая книга Яренского уезда письма В. Ларионова и А. Горохова</h4>
            <p style="font-size:0.85rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
              Древнейшее сохранившееся писцовое описание уезда эпохи Смуты. На погосте Катва (Оквад) зафиксирован самостоятельный тяглый двор молодого домохозяина: <em>«в. МИКИTКА ТУРКИН молотчей»</em> (родной брат патриарха Семёна Туркина).
            </p>
            <div style="font-size:0.8rem; color:var(--text-muted); line-height:1.45; margin-bottom:0.75rem;">
              <strong>Публикация:</strong> «Акты времени Василия Шуйского (1606–1610 гг.)», СПб., 1914, № 103, с. 294; РГАДА, 7116 г., л. 82 об.–83.
            </div>
          </div>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap; padding-top:0.65rem; border-top:1px dashed var(--border-color);">
            <a href="https://www.vostlit.info/Texts/Dokumenty/Russ/XVII/1600-1620/Akty_Vas_Shujskogo/101-120/103_2.htm" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#0369a1; font-weight:600; background:#f0f9ff; border:1px solid #bae6fd;">🌐 Читать на «Восточной Литературе» (№ 103) ↗</a>
            <button onclick="openDocViewerById('ancient_1608_katva_turkin')" class="pill-btn" style="font-size:0.76rem; background:var(--bg-primary); border:1px solid var(--border-color); cursor:pointer;">🔍 Карточка в архиве</button>
          </div>
        </div>

      </div>
    </div>

    <!-- 3. STATE ARCHIVES (RGADA, GAVO, NARK) -->
    <div id="state-archives" class="info-card" style="margin-bottom:1.5rem; border-left: 4px solid #059669;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <div>
          <h3 style="margin:0; font-size:1.22rem; color:#059669;">🏛️ Государственные архивы: фонды, описи и архивные дела</h3>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.15rem;">Официальные дела Поместного приказа, Вологодского архиерейского дома и казённых палат XVII–XIX вв.</div>
        </div>
        <span style="font-size:0.75rem; background:#ecfdf5; color:#059669; font-weight:700; padding:0.25rem 0.65rem; border-radius:20px; border:1px solid #a7f3d0;">РГАДА • ГАВО • НАРК</span>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem;">
        
        <!-- RGADA CARD -->
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <strong style="color:#059669; font-size:1.02rem;">РГАДА (Москва)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.45rem; background:#ecfdf5; color:#059669; border-radius:4px; font-weight:700;">Древние акты</span>
          </div>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:0.6rem;">Российский государственный архив древних актов • <a href="http://rgada.info/" target="_blank" rel="noopener noreferrer" style="color:#059669;">rgada.info ↗</a></div>
          <ul style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin:0 0 0.75rem 1.1rem; padding:0;">
            <li><strong>Ф. 1209, оп. 1, д. 1080 (1646 г.):</strong> Переписная книга воеводы И. Г. Скрябина. Погост Оквад: двор приказного человека Офоньки Семенова сына Туркина с сыном Исачком (11 лет), сын Архипко ушёл в 1643 г. в Сибирь.</li>
            <li><strong>Ф. 1209, оп. 1, д. 1081 (1678 г.):</strong> Перепись стольника Ф. И. Потёмкина. Дьячок Исаак Афанасьев сын Туркин с сыновьями Петром, Тимофеем, Ларионом; бобыль Ипатий Семенов сын Туркин.</li>
            <li><strong>Ф. 1209, оп. 1, д. 1081 (1710 г.):</strong> Ландратская перепись. Церковный пономарь Иван Петрович Туркин 22 года с женой Татьяной и сыном Стефаном.</li>
            <li><strong>Ф. 350, оп. 2, д. 4216 (1748 г.):</strong> 2-я государственная ревизия. Деревня Пальтыдор (Летовы, Ярановы), с. Коквицы (Сизевы).</li>
            <li><strong>Ф. 350, оп. 2, д. 4224, 4232 (1762 г.):</strong> 3-я ревизия податного населения Яренского уезда.</li>
          </ul>
          <div style="display:flex; gap:0.4rem; flex-wrap:wrap; padding-top:0.5rem; border-top:1px dashed var(--border-color);">
            <button onclick="openDocViewerById('ancient_1646_rgada_okvad_turkin')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Перепись 1646 г.</button>
            <button onclick="openDocViewerById('ancient_1678_turkin_yarensk')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Перепись 1678 г.</button>
            <button onclick="openDocViewerById('ancient_1710_rgada_landrat_turkin')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Ландрат 1710 г.</button>
            <button onclick="openDocViewerById('1748_РГАДА_Палтыдор_Летовы_Ярановы')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Ревизия 1748 г.</button>
          </div>
        </div>

        <!-- GAVO / VCA CARD -->
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <strong style="color:#059669; font-size:1.02rem;">ГАВО и ВЦА (Вологда)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.45rem; background:#ecfdf5; color:#059669; border-radius:4px; font-weight:700;">Архиерейский дом</span>
          </div>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:0.6rem;">Государственный архив Вологодской области • <a href="https://gosarchive.gov35.ru/" target="_blank" rel="noopener noreferrer" style="color:#059669;">gosarchive.gov35.ru ↗</a></div>
          <ul style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin:0 0 0.75rem 1.1rem; padding:0;">
            <li><strong>Ф. 1260, оп. 1, д. 1392 (1656 г.):</strong> Судебное дело Вологодского архиерейского дома по челобитной Архипа Туркина архиепископу Маркеллу. Поездка отца Афанасия Туркина в г. Сургут на Оби, заёмные кабалы на 347 рублей серебром.</li>
            <li><strong>ВЦА (Вологодский церковный архив), ф. 496:</strong> Исповедная роспись Христорождественской церкви с. Коквицы 1773 года. Двор № 167: прямая семья Туркиных (Стефан Иванович 62 года, дети Алексей, Иван, Василий).</li>
            <li><strong>Клировые ведомости церквей Яренского уезда:</strong> послужные списки священно- и церковнослужителей Туркиных Введенской церкви Оквада и Христорождественской церкви Коквиц.</li>
          </ul>
          <div style="display:flex; gap:0.4rem; flex-wrap:wrap; padding-top:0.5rem; border-top:1px dashed var(--border-color);">
            <button onclick="openDocViewerById('ancient_1656_gavo_sud_turkin_p1')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Суд 1656 г. (Сургут)</button>
            <button onclick="openDocViewerById('1773_ВЦА_Коквицы_Туркины_Исповедная_роспись')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Исповедка 1773 г.</button>
          </div>
        </div>

        <!-- NARK CARD -->
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <strong style="color:#059669; font-size:1.02rem;">НАРК (Сыктывкар)</strong>
            <span style="font-size:0.72rem; padding:0.1rem 0.45rem; background:#ecfdf5; color:#059669; border-radius:4px; font-weight:700;">Ревизии и метрики</span>
          </div>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-bottom:0.6rem;">Национальный архив Республики Коми • <a href="https://archive.rkomi.ru/" target="_blank" rel="noopener noreferrer" style="color:#059669;">archive.rkomi.ru ↗</a></div>
          <ul style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin:0 0 0.75rem 1.1rem; padding:0;">
            <li><strong>Ф. 231 (Яренское уездное казначейство):</strong> 10-я ревизия 1858 г. — д. Сюлатуй (Иван Туркин с сыном Алексеем 6 лет), д. Ероздино (Шуктомовы), д. Горелый Ыб (Зиновьевы).</li>
            <li><strong>Ф. 231:</strong> Ревизские сказки 9-й (1850 г.), 8-й (1834 г.), 7-й (1816 г.) ревизий селений Коквицкой, Часовской и Усть-Вымской волостей.</li>
            <li><strong>Ф. 255 (Духовная консистория):</strong> Метрические книги Коквицкой Христорождественской церкви (запись о рождении Николая Алексеевича Туркина в 1876 г., Михаила Николаевича Туркина в 1906 г.).</li>
            <li><strong>Ф. 255:</strong> Метрические книги Часовской Спасской церкви (запись о рождении Евгения Александровича Шуктомова в 1908 г. в д. Ероздино).</li>
          </ul>
          <div style="display:flex; gap:0.4rem; flex-wrap:wrap; padding-top:0.5rem; border-top:1px dashed var(--border-color);">
            <button onclick="openDocViewerById('1858_Ревизия_Сюлатуй_Туркины')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Ревизия 1858 г. (Сюлатуй)</button>
            <button onclick="openDocViewerById('1876_Метрика_Николай_Туркин')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Метрика 1876 г.</button>
            <button onclick="openDocViewerById('1906_Метрика_Михаил_Туркин')" class="pill-btn" style="font-size:0.72rem; cursor:pointer;">Метрика 1906 г.</button>
          </div>
        </div>

      </div>
    </div>

    <!-- 4. MILITARY ARCHIVES (WW2 1941–1945) -->
    <div id="ww2-archives" class="info-card" style="margin-bottom:1.5rem; border-left: 4px solid #dc2626;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <div>
          <h3 style="margin:0; font-size:1.22rem; color:#dc2626;">🎖️ Военные архивы и электронные банки документов (ВОВ 1941–1945 гг.)</h3>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.15rem;">Фронтовые приказы, наградные листы и журналы боевых действий Центрального архива Министерства обороны РФ</div>
        </div>
        <span style="font-size:0.75rem; background:#fef2f2; color:#dc2626; font-weight:700; padding:0.25rem 0.65rem; border-radius:20px; border:1px solid #fecaca;">ЦАМО РФ • Подвиг Народа</span>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1.25rem;">
        
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:var(--text-main);">🌐 Государственный портал «Память Народа»</h4>
          <p style="font-size:0.84rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
            Официальный общедоступный банк подлинных документов о фронтовиках и войсковых операциях ВОВ, созданный Министерством обороны РФ:
          </p>
          <ul style="font-size:0.83rem; line-height:1.5; color:var(--text-main); margin:0 0 0.75rem 1.1rem; padding:0;">
            <li><strong>Зиновьев Владимир Семенович (1918–1945):</strong> гвардии майор, кавалер орденов Александра Невского, Красного Знамени, Отечественной войны I и II ст., медали «За отвагу», участник штурма Берлина;</li>
            <li><strong>Зиновьев Семён Григорьевич (род. 1896):</strong> старший сержант артиллерии, медаль «За отвагу», благодарность Сталина № 372 за Маньчжурскую операцию.</li>
          </ul>
          <a href="https://pamyat-naroda.ru/" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#dc2626; font-weight:600; background:#fef2f2; border:1px solid #fecaca;">🌐 Перейти на pamyat-naroda.ru ↗</a>
        </div>

        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:var(--text-main);">🌐 Банк данных «Подвиг Народа в Великой Отечественной войне»</h4>
          <p style="font-size:0.84rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
            Электронная база оцифрованных наградных листов с описаниями личных подвигов воинов, выписками из боевых приказов и представлениями к орденам и медалям СССР.
          </p>
          <a href="http://podvignaroda.ru/" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#dc2626; font-weight:600; background:#fef2f2; border:1px solid #fecaca;">🌐 Перейти на podvignaroda.ru ↗</a>
        </div>

        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:var(--text-main);">🌐 Обобщенный банк данных «ОБД Мемориал»</h4>
          <p style="font-size:0.84rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
            Банк данных об участниках войны, госпитальных книгах и воинских захоронениях защитников Отечества, погибших и пропавших без вести.
          </p>
          <a href="https://obd-memorial.ru/" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#dc2626; font-weight:600; background:#fef2f2; border:1px solid #fecaca;">🌐 Перейти на obd-memorial.ru ↗</a>
        </div>

      </div>
    </div>

    <!-- 5. ONLINE DATABASES AND SCHOLARLY RESEARCH -->
    <div id="online-databases" class="info-card" style="margin-bottom:1.5rem; border-left: 4px solid #7c3aed;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <div>
          <h3 style="margin:0; font-size:1.22rem; color:#7c3aed;">🌐 Научно-генеалогические базы данных, каталоги и исследования</h3>
          <div style="font-size:0.82rem; color:var(--text-muted); margin-top:0.15rem;">Специализированные научные порталы, исторические исследования и сетевые форумы родоведов</div>
        </div>
        <span style="font-size:0.75rem; background:#f5f3ff; color:#7c3aed; font-weight:700; padding:0.25rem 0.65rem; border-radius:20px; border:1px solid #ddd6fe;">Базы данных</span>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:1.25rem;">
        
        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:#7c3aed;">⛪ Православные приходы и монастыри Севера</h4>
          <p style="font-size:0.84rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
            Научная база данных северного духовенства. Раздел <strong>«Персоналии № 57: Туркины»</strong> документирует династию священно- и церковнослужителей Введенской церкви Оквада и Христорождественской церкви Коквиц (дьячок Исаакий Афанасьевич, пономарь Иван Петрович, иерей Автоном Лаврентьевич и др.).
          </p>
          <a href="http://parishes.ru/pers.php?no=57#14873" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#7c3aed; font-weight:600; background:#f5f3ff; border:1px solid #ddd6fe;">🌐 Персоналии духовенства: Туркины (parishes.ru) ↗</a>
        </div>

        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:#7c3aed;">🌳 Форум «Всероссийское Генеалогическое Древо» (ВГД)</h4>
          <p style="font-size:0.84rem; line-height:1.55; color:var(--text-main); margin-bottom:0.6rem;">
            Крупнейший русскоязычный генеалогический портал. Тематические разделы по Яренскому уезду, Вологодской епархии, Коквицкой волости и архивам Республики Коми, аккумулирующие опыт сотен исследователей.
          </p>
          <a href="https://forum.vgd.ru/" target="_blank" rel="noopener noreferrer" class="pill-btn" style="font-size:0.76rem; text-decoration:none; color:#7c3aed; font-weight:600; background:#f5f3ff; border:1px solid #ddd6fe;">🌐 Генеалогический форум ВГД ↗</a>
        </div>

        <div style="background:var(--bg-surface); border-radius:10px; border:1px solid var(--border-color); padding:1.15rem;">
          <h4 style="margin:0 0 0.4rem 0; font-size:1.02rem; color:#7c3aed;">📖 Научные монографии и публикации</h4>
          <ul style="font-size:0.83rem; line-height:1.55; color:var(--text-main); margin:0; padding-left:1.1rem;">
            <li><strong>Башнин Н. В.</strong> «Сшел в Сибирь»: миграция населения яренской вотчины Вологодского архиерейского дома в XVII в. // «Институты и общности», 2019, с. 135–136.</li>
            <li><strong>Доронин П. Г.</strong> «Вычегодско-Вымская (Мисаило-Евтихиевская) летопись» // Историко-филологический сборник, Сыктывкар, 1958.</li>
            <li><strong>Мацук М. А.</strong> «Город Яренск и Яренский уезд в переписях XVII века», Сыктывкар, Коми НЦ УрО РАН.</li>
          </ul>
        </div>

      </div>
    </div>

    <!-- 6. INTERACTIVE ARCHIVE OF THIS PROJECT -->
    <div class="info-card" style="background:linear-gradient(135deg, rgba(37,99,235,0.06), rgba(5,150,105,0.06)); border:1.5px solid var(--accent);">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div>
          <h3 style="margin:0 0 0.35rem 0; font-size:1.15rem; color:var(--accent);">🔍 Интерактивный архив первоисточников в составе приложения</h3>
          <p style="margin:0; font-size:0.88rem; color:var(--text-main); line-height:1.5;">
            В специальном разделе <strong>«Архив документов»</strong> доступно <strong>{len(archive_catalog.DOCS_CATALOG)} оцифрованных архивных первоисточников</strong> высокого разрешения с детальными текстовыми расшифровками, источниковедческими справками и полноэкранным увеличением.
          </p>
        </div>
        <button class="pill-btn" onclick="switchTab('archive')" style="font-size:0.85rem; padding:0.5rem 1.1rem; background:var(--accent); color:#fff; border:none; cursor:pointer; font-weight:700; box-shadow:0 3px 8px rgba(37,99,235,0.3);">🏛️ Открыть каталог архивных документов ({len(archive_catalog.DOCS_CATALOG)})</button>
      </div>
    </div>

    <!-- BOTTOM ANCHOR NAVIGATION BAR FOR SOURCES -->
    <nav class="info-bottom-bar" id="sourcesBottomBar">
      <div class="info-bottom-scroll">
        <a href="#books-series" class="info-bottom-pill active" onclick="scrollToAnchor(event, 'books-series')">
          <span>📖</span> <span class="pill-lbl-full">Книги</span><span class="pill-lbl-short">Книги</span>
        </a>
        <a href="#ancient-chronicles" class="info-bottom-pill" onclick="scrollToAnchor(event, 'ancient-chronicles')">
          <span>📜</span> <span class="pill-lbl-full">Летописи</span><span class="pill-lbl-short">Акты</span>
        </a>
        <a href="#state-archives" class="info-bottom-pill" onclick="scrollToAnchor(event, 'state-archives')">
          <span>🏛️</span> <span class="pill-lbl-full">Гос. архивы</span><span class="pill-lbl-short">Архивы</span>
        </a>
        <a href="#ww2-archives" class="info-bottom-pill" onclick="scrollToAnchor(event, 'ww2-archives')">
          <span>🎖️</span> <span class="pill-lbl-full">Архивы ВОВ</span><span class="pill-lbl-short">ВОВ</span>
        </a>
        <a href="#online-databases" class="info-bottom-pill" onclick="scrollToAnchor(event, 'online-databases')">
          <span>🌐</span> <span class="pill-lbl-full">Базы данных</span><span class="pill-lbl-short">Базы</span>
        </a>
      </div>
    </nav>
  </div>

  <!-- TAB 5: STATS VIEW -->
  <div id="view-stats" class="view-section">
    <div class="stats-grid" style="grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
      <div class="stat-box">
        <div class="stat-number">{total_persons}</div>
        <div class="stat-label">Всего персон в древе</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{total_families}</div>
        <div class="stat-label">Брачных союзов</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">15</div>
        <div class="stat-label">Документированных поколений</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{len(archive_catalog.DOCS_CATALOG)}</div>
        <div class="stat-label">Архивных первоисточников</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{male_count} / {female_count}</div>
        <div class="stat-label">Мужчин (69%) / Женщин (31%)</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">416+ лет</div>
        <div class="stat-label">Летопись рода (1608–2024 гг.)</div>
      </div>
    </div>

    <!-- DIRECT MALE LINEAGE TIMELINE -->
    <div class="info-card">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <h2 style="margin:0;">🏛️ Непрерывная прямая мужская линия Туркиных (15 поколений, 1608–2024 гг.)</h2>
        <span style="font-size:0.8rem; font-weight:700; color:#059669; background:#ecfdf5; padding:0.25rem 0.6rem; border-radius:6px; border:1px solid #a7f3d0;">100% документальная преемственность</span>
      </div>
      <p style="font-size:0.86rem; color:var(--text-muted); margin-bottom:1rem; line-height:1.5;">
        На основе архивных первоисточников РГАДА, ГАВО, НА РК, ВУЦА и МК полностью реконструирована непрерывная цепочка прямой отцовской линии от Смутного времени до современности:
      </p>

      <div style="overflow-x:auto;">
        <table class="data-table" style="font-size:0.83rem; width:100%;">
          <thead>
            <tr>
              <th style="width:60px;">Колено</th>
              <th>Персона (Прямой предок)</th>
              <th>Годы жизни / Статус</th>
              <th>Архивный первоисточник</th>
              <th style="width:45px; text-align:center;">Древо</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>I</strong></td>
              <td><strong>Николай Вячеславович Туркин</strong></td>
              <td>род. 2024 • Пробанд рода</td>
              <td>Свидетельство о рождении, г. Чумпхон (Таиланд)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I1'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>II</strong></td>
              <td><strong>Вячеслав Михайлович Туркин</strong></td>
              <td>род. 1991 • Отец</td>
              <td>Семейный архив, г. Сыктывкар</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I2'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>III</strong></td>
              <td><strong>Михаил Аркадьевич Туркин</strong></td>
              <td>род. 1970 • Дедушка</td>
              <td>Семейный архив, г. Сыктывкар</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I9'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>IV</strong></td>
              <td><strong>Аркадий Михайлович Туркин</strong></td>
              <td>03.09.1935 – 17.01.2000 • Прадедушка</td>
              <td>Семейный архив, с. Коквицы</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I13'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>V</strong></td>
              <td><strong>Михаил Николаевич Туркин</strong></td>
              <td>1906–1993 • Прапрадед, гв. ст. сержант ВОВ</td>
              <td>ЦАМО РФ, наградные листы 1943–1945 гг.</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I19'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>VI</strong></td>
              <td><strong>Николай Алексеевич Туркин</strong></td>
              <td>род. 03.11.1876 • 3-й прадед</td>
              <td>НА РК, Метрическая книга с. Коквицы (с. 267)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I25'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>VII</strong></td>
              <td><strong>Алексей Иванович Туркин</strong></td>
              <td>род. 1852 • 4-й прадед</td>
              <td>10-я ревизия 1858 г., 9-я ревизия 1850 г. (НА РК)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I43'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>VIII</strong></td>
              <td><strong>Иван Алексеевич Туркин</strong></td>
              <td>род. ок. 1825 • 5-й прадед</td>
              <td>8-я ревизия 1834 г. (ГАВО, ф. 388, оп. 10, д. 70, л. 168)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I70'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>IX</strong></td>
              <td><strong>Алексей Григорьевич Туркин</strong></td>
              <td>род. ок. 1778 • 6-й прадед</td>
              <td>8-я ревизия 1834 г., 4-я ревизия 1782 г. (ГАВО)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I148'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>X</strong></td>
              <td><strong>Григорий Степанович Туркин</strong></td>
              <td>род. 1751 • 7-й прадед</td>
              <td>Исповедная роспись 1773 г., двор 167 (ВЦА, ф. 363)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I80'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>XI</strong></td>
              <td><strong>о. Степан Иванович Туркин</strong></td>
              <td>род. ок. 1711 • 8-й прадед, священник (иерей)</td>
              <td>Исповедная роспись 1773 г., Ландратская 1710 г. (РГАДА)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I78'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>XII</strong></td>
              <td><strong>Иван Петрович Туркин</strong></td>
              <td>род. 1688 • 9-й прадед, церковный пономарь</td>
              <td>Ландратская перепись 1710 г. (РГАДА, ф. 1209, д. 1081)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I71'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr>
              <td><strong>XIII</strong></td>
              <td><strong>о. Пётр Исаакович Туркин</strong></td>
              <td>род. ок. 1655–1661 • 10-й прадед, священник</td>
              <td>Перепись 1678 г. (РГАДА), Метрическая книга 1731 г. (ГААО)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I72'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.04);">
              <td><strong>XIV</strong></td>
              <td><strong>Исаак Афанасьевич Туркин</strong></td>
              <td>род. 1635 • 11-й прадед, церковный дьячок</td>
              <td>Перепись 1646 г. (11 лет), Перепись 1678 г. (дьячок)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I73'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.08); font-weight:600;">
              <td><strong>XV</strong></td>
              <td><strong>Афанасий Семёнович Туркин</strong></td>
              <td>род. ок. 1600 • 12-й прадед, архиепископский приказной</td>
              <td>Переписная книга воеводы И. Г. Скрябина 1646 г. (РГАДА ф. 1209, д. 1080)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I74'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
            <tr style="background:rgba(37,99,235,0.12); font-weight:700;">
              <td><strong>XVI</strong></td>
              <td><strong>Семён Туркин</strong> (брат Микитки Туркина)</td>
              <td>род. ок. 1575–1580 • 13-й прадед, родоначальник</td>
              <td>Дозорная книга Яренского уезда 1608 г. (РГАДА)</td>
              <td style="text-align:center;"><button class="pill-btn" onclick="focusPerson('I274'); switchTab('tree');" style="font-size:0.72rem;">🎯</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- STATS BY EPOCHS AND SURNAMES -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:1.25rem;">
      <!-- EPOCHS CARD -->
      <div class="info-card">
        <h3 style="margin-top:0; color:#2563eb;">⏳ Распределение по историческим эпохам</h3>
        <ul style="font-size:0.86rem; line-height:1.6; margin:0; padding-left:1.15rem;">
          <li><strong>XVII век (1601–1700 гг.) — 64 персоны (33%):</strong> эпоха становления приказного аппарата Вологодского архиерейского дома, дьячков и священнослужителей.</li>
          <li><strong>XVIII век (1701–1800 гг.) — 46 персон (23%):</strong> разветвление духовного сословия (Коквицы, Оквад, Усть-Вымь, Палевицы), первые ревизские сказки и исповедные росписи.</li>
          <li><strong>XIX век (1801–1900 гг.) — 32 персоны (16%):</strong> государственные крестьяне Коквицкой волости, соборный клир Лальска, общины Ыба, Ероздино и Лоймы.</li>
          <li><strong>XX век (1901–2000 гг.) — 24 персоны (12%):</strong> участники Великой Отечественной войны, труженики тыла, новомученики и исповедники Севера.</li>
          <li><strong>XXI век (2001–н.в.) — современное поколение:</strong> международная ветвь семьи (Россия — Таиланд).</li>
          <li><strong>XVI век и ранее:</strong> патриархи и древнейшие родоначальники Вычегды.</li>
        </ul>
      </div>

      <!-- SURNAMES CARD -->
      <div class="info-card">
        <h3 style="margin-top:0; color:#7c3aed;">🧬 Распределение по родам и фамилиям</h3>
        <ul style="font-size:0.86rem; line-height:1.6; margin:0; padding-left:1.15rem;">
          <li><strong>Род Туркиных:</strong> 139 персон (70.6% древа) — вычегодская священническая и крестьянская династия.</li>
          <li><strong>Коми ветви предков:</strong> 50 персон (Сюткины, Шехонины, Шуктомовы, Зиновьевы, Летовы, Полещиковы, Пасынковы, Кызъюровы, Поздеевы, Каракчиевы, Ярановы, Сизевы, Айбабины, Кругляковы, Шилины).</li>
          <li><strong>Тайские роды:</strong> 8 персон (Питак, Памайтонг, Чамнианкан).</li>
          <li><strong>Архивная полнота:</strong> 100% персон связаны семейными узами и архивными первоисточниками.</li>
        </ul>
      </div>
    </div>
  </div>
</main>

<!-- BIOGRAPHICAL PROFILE MODAL -->
<!-- INTERACTIVE DOCUMENT LIGHTBOX VIEWER -->
<div class="doc-viewer-modal" id="docViewerModal" onclick="closeDocViewerOnOverlay(event)">
  <div class="doc-viewer-container" onclick="event.stopPropagation()">
    <!-- VIEWER HEADER -->
    <div class="doc-viewer-header">
      <div class="doc-viewer-title-group" style="min-width:0; flex:1;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.2rem;">
          <span class="doc-viewer-badge" id="docViewerBadge">ЦАМО РФ</span>
          <span id="docViewerPerson" style="font-size:0.8rem; font-weight:600; color:var(--text-muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"></span>
        </div>
        <h3 id="docViewerTitle" style="margin:0; font-size:1.02rem; line-height:1.3; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Название документа</h3>
        <div id="docViewerArchive" style="font-size:0.75rem; color:var(--text-muted); margin-top:0.2rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Архивные реквизиты</div>
      </div>
      <div class="doc-viewer-actions">
        <button class="doc-close-btn" onclick="closeDocViewer()" title="Закрыть документ и вернуться в карточку (Esc)">
          <span style="font-size:1.05rem; line-height:1;">✕</span> <span>Назад</span>
        </button>
      </div>
    </div>

    <!-- VIEWER VIEWPORT WITH ZOOM AND PAN -->
    <div class="doc-viewer-viewport" id="docViewerViewport">
      <button class="doc-nav-btn prev" id="docNavPrev" onclick="docPrev()" title="Предыдущий документ (←)">❮</button>
      <div class="doc-img-wrapper" id="docImgWrapper" title="Нажмите на скан, чтобы открыть на весь экран с возможностью зума" style="cursor:pointer; position:relative;">
        <img id="docViewerImg" src="" alt="Архивный документ" draggable="false" />
        <div class="doc-img-hint-badge">🔍 Открыть скан на весь экран (зум)</div>
      </div>
      <button class="doc-nav-btn next" id="docNavNext" onclick="docNext()" title="Следующий документ (→)">❯</button>
    </div>

    <!-- VIEWER FOOTER -->
    <div class="doc-viewer-footer">
      <div class="doc-viewer-footer-text">
        <div id="docViewerDesc" style="font-size:0.82rem; line-height:1.45; color:var(--text-main);"></div>
      </div>
      <div style="display:flex; align-items:center; gap:0.6rem; flex-shrink:0;">
        <button class="pill-btn" onclick="closeDocViewer()" style="font-size:0.75rem; background:var(--bg-primary); border-color:var(--border-color); color:var(--text-main); cursor:pointer;">✕ Назад</button>
        <div class="doc-viewer-footer-counter" id="docViewerCounter">
          1 / 19
        </div>
      </div>
    </div>
  </div>
</div>

<!-- FULLSCREEN SCAN LIGHTBOX MODAL WITH ZOOM & PAN -->
<div id="fsScanModal" class="fs-scan-modal" role="dialog" aria-modal="true" aria-labelledby="fsScanTitle" onclick="closeFsScanOnOverlay(event)">
  <div class="fs-scan-header" onclick="event.stopPropagation()">
    <div class="fs-scan-info">
      <div class="fs-scan-title" id="fsScanTitle">Оригинал документа</div>
      <div class="fs-scan-meta" id="fsScanMeta"></div>
    </div>
    <div class="fs-scan-tools">
      <button class="fs-tool-btn" onclick="fsZoomOut()" title="Уменьшить (−)">🔍−</button>
      <button class="fs-tool-btn" onclick="fsResetZoom()" id="fsZoomLabel" title="Сбросить масштаб (1:1 / 100%)">100%</button>
      <button class="fs-tool-btn" onclick="fsZoomIn()" title="Увеличить (+)">🔍+</button>
      <button class="fs-close-btn" onclick="closeFsScan()" title="Закрыть скан (Esc)">
        <span>✕</span> <span>Закрыть</span>
      </button>
    </div>
  </div>
  <div class="fs-scan-viewport" id="fsScanViewport">
    <div class="fs-scan-img-container" id="fsScanImgContainer">
      <img id="fsScanImg" src="" alt="Оригинал скана" draggable="false" />
    </div>
  </div>
  <div class="fs-floating-tools" onclick="event.stopPropagation()">
    <button class="fs-float-btn" onclick="fsZoomOut()" title="Уменьшить (−)">🔍−</button>
    <button class="fs-float-btn" onclick="fsResetZoom()" title="Сбросить масштаб (1:1)">↺ 1:1</button>
    <button class="fs-float-btn" onclick="fsZoomIn()" title="Увеличить (+)">🔍+</button>
    <button class="fs-float-btn fs-float-close" onclick="closeFsScan()" title="Закрыть скан (Esc)">✕ Закрыть</button>
  </div>
</div>

<div class="modal-overlay" id="personModal" onclick="closeModalOnOverlay(event)">
  <div class="modal-card">
    <div class="modal-header">
      <div class="modal-title">
        <h2 id="modalName">ФИО</h2>
        <div id="modalSubtitle" style="font-size:0.82rem; color:var(--text-muted); margin-top:0.25rem;"></div>
      </div>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<script>
const INDIS = {indis_json};
const FAMS = {fams_json};
const DOCS = {docs_json};
const PDFS = {pdfs_json};

let currentTab = 'tree';
let zoom = 0.85;
let panX = 60;
let panY = 80;
let isDragging = false;
let startX, startY;
let showArrows = true; // or 'parent_to_child'
let showSpouses = true;
let hoveredPersonId = null;
let onlyDirectLine = false;
const directAncestorIds = new Set();

function computeDirectAncestorIds() {{
  directAncestorIds.clear();
  function traverse(id) {{
    if (!id || !INDIS[id] || directAncestorIds.has(id)) return;
    directAncestorIds.add(id);
    const p = INDIS[id];
    if (p.father_id) traverse(p.father_id);
    if (p.mother_id) traverse(p.mother_id);
  }}
  traverse('I1');
}}

const genTitles = [
  "",
  "Поколение I (Пробанд • 1995/2024)",
  "Поколение II (Родители • 1970–1991)",
  "Поколение III (Дедушки и бабушки • 1935–1970)",
  "Поколение IV (Прадедушки и прабабушки • 1906–1935)",
  "Поколение V (Прапрадедушки • 1876–1906)",
  "Поколение VI (3-й прадед • Николай Алексеевич • 1876 г.р.)",
  "Поколение VII (4-й прадед • Алексей Иванович • 1852 г.р.)",
  "Поколение VIII (5-й прадед • Иван Алексеевич • ок. 1825 г.р. • 8-я ревизия 1834 г.)",
  "Поколение IX (6-й прадед • Алексей Григорьевич • ок. 1778 г.р. • 8-я ревизия 1834 г.)",
  "Поколение X (7-й прадед • Григорий Степанович • 1751 г.р. • Исповедная роспись 1773 г.)",
  "Поколение XI (8-й прадед • Степан Иванович • ок. 1720 г.р.)",
  "Поколение XII (9-й прадед • Пономарь Иван Туркин • Перепись 1710 г.)",
  "Поколение XIII (10-й прадед • Священник Пётр Туркин • Перепись 1678 г.)",
  "Поколение XIV (11-й прадед • Дьячок Исаак Туркин • Перепись 1678 г.)",
  "Поколение XV (13-й прадед • Приказной Афанасий Туркин • Перепись 1646 г.)",
  "Поколение XVI (14-й прадед • Патриарх рода Семён Туркин • рубеж XVI–XVII вв.)",
  "Поколение XVII (15-й прадед • Отец Семёна Туркина • ок. 1545 г.р. • XVI в.)",
  "Поколение XVIII (16-й прадед • Внук Турки малого • ок. 1515 г.р. • XVI в.)",
  "Поколение XIX (17-й прадед • Сын Турки малого • ок. 1485 г.р. • XVI в.)",
  "Поколение XX (18-й прадед • Прародитель рода Турка малой • Грамота 1490 г.)"
];

function init() {{
  computeDirectAncestorIds();
  renderPinnedGenHeaders();
  renderTreeCards();
  renderSvgLinks();
  renderGenerations();
  renderTable();
  renderArchiveGrid();
  setupCanvasDrag();
  setupDocViewerEvents();
  setupFsScanEvents();
  centerOnRoot();
  setupHashRouting();
}}

function switchTab(tabId) {{
  currentTab = tabId;
  document.querySelectorAll('.nav-tab').forEach((b) => {{
    const onclickAttr = b.getAttribute('onclick') || '';
    b.classList.toggle('active', onclickAttr.includes(`switchTab('${{tabId}}')`));
  }});
  document.querySelectorAll('.drawer-nav-item').forEach((b) => {{
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  }});
  document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));
  const targetView = document.getElementById(`view-${{tabId}}`);
  if (targetView) targetView.classList.add('active');

  if (tabId === 'tree') {{
    updateTransform();
  }}
}}

// PINNED GENERATION HEADERS (ALIGNED TO COLUMNS, STAYS AT TOP)
function renderPinnedGenHeaders() {{
  const track = document.getElementById('pinnedGenTrack');
  track.innerHTML = '';
  const genXMap = {{
    1: 80, 2: 440, 3: 800, 4: 1160, 5: 1520, 6: 1880, 7: 2240, 8: 2600, 9: 2960,
    10: 3320, 11: 3680, 12: 4040, 13: 4400, 14: 4760, 15: 5120, 16: 5480,
    17: 5840, 18: 6200, 19: 6560, 20: 6920
  }};
  for (let g = 1; g <= 20; g++) {{
    const div = document.createElement('div');
    div.className = 'pinned-gen-title';
    div.setAttribute('data-gen', g);
    div.style.left = `${{genXMap[g]}}px`;
    div.textContent = genTitles[g];
    div.title = `Нажмите, чтобы центрировать древо по поколению ${{g}}`;
    div.onclick = (e) => {{
      e.stopPropagation();
      focusGeneration(g);
    }};
    track.appendChild(div);
  }}
}}

function getPersonSourceInfo(p) {{
  if (!p) return null;

  let num = 0;
  try {{
    num = parseInt(p.id.replace('I', ''));
  }} catch(e) {{}}

  if (num >= 314 && num <= 332) {{
    return {{
      type: 'text',
      text: 'Заполнено по информации из личного семейного архива (родословное древо Олега Лычковского, с. Лойма).'
    }};
  }}

  const gen = p.gen || 1;
  if (gen <= 4) {{
    // С 1 по 4 поколения: никаких документов и источников
    return null;
  }}

  // Линии семейных предков: 5-6 поколения, 7 поколение (I43-I62, I333), 8 поколение (Харлампий Пасынков I63, Параскева Круглякова I64, Иона Каракчиев I65), 9 поколение (Мария Круглякова I66)
  const isFamilyArchivePerson = (gen === 5 || gen === 6) ||
    ['I63', 'I64', 'I65', 'I66', 'I333'].includes(p.id) ||
    (p.name && p.name.includes('Кругляков')) ||
    (gen === 7 && num >= 43 && num <= 62);

  if (isFamilyArchivePerson) {{
    return {{
      type: 'text',
      text: 'Заполнено по информации из личных семейных архивов и при помощи «Усть-Вымского Родословия» (тома 1–3, авторы: Людмила Владимировна Ванеева, Валентина Александровна Гусева, Лидия Афанасьевна Молодцова).'
    }};
  }}

  return {{
    type: 'archive'
  }};
}}

function getPersonDocs(pid) {{
  const p = INDIS[pid];
  if (!p) return [];
  if (p.gen <= 4) return [];
  return DOCS.filter(d => d.personId === pid || (d.personIds && d.personIds.includes(pid)));
}}

// RENDER ALL CARDS AT EXACT (X, Y)
function renderTreeCards() {{
  const container = document.getElementById('cardsLayer');
  container.innerHTML = '';

  Object.values(INDIS).forEach(p => {{
    const personDocs = getPersonDocs(p.id);
    const hasDocs = personDocs.length > 0;
    const isReconstructed = !!p.is_reconstructed;
    const isDirect = directAncestorIds.has(p.id);
    const isHidden = onlyDirectLine && !isDirect;
    const card = document.createElement('div');
    card.className = `person-card sex-${{p.sex}} ${{p.id === 'I1' ? 'is-proband' : ''}} ${{hasDocs ? 'has-archival-docs' : ''}} ${{isReconstructed ? 'is-reconstructed' : ''}} ${{isHidden ? 'is-hidden-branch' : ''}}`;
    card.id = `card-${{p.id}}`;
    card.style.left = `${{p.x}}px`;
    card.style.top = `${{p.y}}px`;

    let downX = 0, downY = 0, isMoved = false;
    card.addEventListener('pointerdown', (e) => {{
      downX = e.clientX;
      downY = e.clientY;
      isMoved = false;
    }});
    card.addEventListener('pointermove', (e) => {{
      if (Math.hypot(e.clientX - downX, e.clientY - downY) > 8) {{
        isMoved = true;
      }}
    }});
    card.onclick = (e) => {{
      e.stopPropagation();
      if (isMoved) return;
      openModal(p.id);
    }};

    card.onmouseenter = () => highlightLineage(p.id);
    card.onmouseleave = () => clearHighlight();

    const sexIcon = p.sex === 'M' ? '♂' : '♀';
    const dates = p.display_birt ? `${{p.display_birt}}${{p.display_deat ? ' – ' + p.display_deat : ''}}` : (p.display_deat ? `ум. ${{p.display_deat}}` : '');
    const isVeteran = (p.id === 'I19' || p.id === 'I67' || p.id === 'I68' || p.id === 'I25' || p.id === 'I23' || p.id === 'I21' || p.id === 'I314' || p.id === 'I315' || p.id === 'I400' || p.id === 'I407' || p.id === 'I408' || p.id === 'I417' || p.id === 'I414' || p.id === 'I417');
    let vetBadge = '';
    if (p.id === 'I400' || p.id === 'I414' || p.id === 'I417') {{
      vetBadge = '<span class="badge-veteran" style="background:#fee2e2; color:#991b1b; border:1px solid #f87171;" title="Участник Отечественной войны 1812 года (рекрут / ратник-стрелок Вологодского ополчения)">🎖️ 1812 г.</span>';
    }} else if (p.id === 'I407' || p.id === 'I408' || p.id === 'I417') {{
      vetBadge = '<span class="badge-veteran" style="background:#ffedd5; color:#9a3412; border:1px solid #fb923c;" title="Участник Заграничного похода русской армии 1813 года (рекрут 1813 г.)">🎖️ 1813 г.</span>';
    }} else if (p.id === 'I25') {{
      vetBadge = '<span class="badge-veteran" title="Ветеран Первой мировой и Великой Отечественной войн">🎖️ ПМВ / ВОВ</span>';
    }} else if (p.id === 'I21') {{
      vetBadge = '<span class="badge-veteran" title="Младший лейтенант ВОВ, кавалер Ордена Отечественной войны I степени">🎖️ ВОВ</span>';
    }} else if (p.id === 'I314' || p.id === 'I315') {{
      vetBadge = '<span class="badge-veteran" title="Участник Великой Отечественной войны (погиб на фронте в 1942 г.)">🎖️ ВОВ</span>';
    }} else if (p.id === 'I68' || p.id === 'I23') {{
      vetBadge = '<span class="badge-veteran" title="Участник Великой Отечественной войны">🎖️ ВОВ</span>';
    }} else if (isVeteran) {{
      vetBadge = '<span class="badge-veteran" title="Герой Великой Отечественной войны">🎖️ ВОВ</span>';
    }}

    let reconBadge = '';
    if (isReconstructed) {{
      reconBadge = '<span class="badge-reconstructed" title="Научная реконструкция промежуточного поколения XVI века (акты утрачены)">⏳ XVI в.</span>';
    }}

    let docBadge = '';
    if (hasDocs) {{
      const firstDocIdx = DOCS.indexOf(personDocs[0]);
      docBadge = `<span class="badge-doc-tree" onclick="event.stopPropagation(); openDocViewer(${{firstDocIdx}}, getPersonDocs('${{p.id}}'));" title="Смотреть архивные документы (${{personDocs.length}})">🏛️ ${{personDocs.length}}</span>`;
    }}

    card.innerHTML = `
      <div class="card-anchor left"></div>
      <div class="card-anchor right"></div>
      <div class="card-top">
        <span class="card-gen" onclick="event.stopPropagation(); focusGeneration(${{p.gen}});" title="Центрировать древо по поколению ${{p.gen}}">Пок. ${{p.gen}}</span>
        <div style="display:flex; align-items:center; gap:0.25rem;">
          ${{reconBadge}}
          ${{docBadge}}
          ${{vetBadge}}
          <span class="card-sex" style="color:${{p.sex === 'M' ? 'var(--male-border)' : 'var(--female-border)'}};">${{sexIcon}}</span>
        </div>
      </div>
      <div class="card-name" title="${{escapeHtml(p.clean_name)}}">${{escapeHtml(p.clean_name)}}</div>
      <div class="card-meta">
        <span class="card-dates">${{dates || '—'}}</span>
        <span class="card-place" title="${{escapeHtml(p.birt_plac)}}">${{p.birt_plac ? '📍 ' + escapeHtml(p.birt_plac) : ''}}</span>
      </div>
      <div class="card-tag" style="background:${{p.branch_color}}18; color:${{p.branch_color}};">${{p.branch}}</div>
    `;

    container.appendChild(card);
  }});
}}

// RENDER SVG BEZIER PATHS & ARROWS
function renderSvgLinks() {{
  const linksG = document.getElementById('svgLinksLayer');
  const spouseG = document.getElementById('svgSpouseLayer');
  linksG.innerHTML = '';
  spouseG.innerHTML = '';

  const CARD_W = 240;
  const CARD_H = 75;

  // 1. Parent - Child Connections
  Object.values(INDIS).forEach(child => {{
    if (onlyDirectLine && !directAncestorIds.has(child.id)) return;
    const cx = child.x + CARD_W;
    const cy = child.y + CARD_H / 2;

    // Father link
    if (child.father_id && INDIS[child.father_id]) {{
      if (!onlyDirectLine || directAncestorIds.has(child.father_id)) {{
        const father = INDIS[child.father_id];
        const fx = father.x;
        const fy = father.y + CARD_H / 2;
        linksG.appendChild(createBezierLink(child.id, father.id, cx, cy, fx, fy, 'father'));
      }}
    }}

    // Mother link
    if (child.mother_id && INDIS[child.mother_id]) {{
      if (!onlyDirectLine || directAncestorIds.has(child.mother_id)) {{
        const mother = INDIS[child.mother_id];
        const mx = mother.x;
        const my = mother.y + CARD_H / 2;
        linksG.appendChild(createBezierLink(child.id, mother.id, cx, cy, mx, my, 'mother'));
      }}
    }}
  }});

  // 2. Spouse links
  if (showSpouses) {{
    const drawnCouples = new Set();
    FAMS.forEach(f => {{
      const hId = f.husb;
      const wId = f.wife;
      if (hId && wId && INDIS[hId] && INDIS[wId]) {{
        if (onlyDirectLine && (!directAncestorIds.has(hId) || !directAncestorIds.has(wId))) return;
        const pairKey = [hId, wId].sort().join('-');
        if (!drawnCouples.has(pairKey)) {{
          drawnCouples.add(pairKey);
          const h = INDIS[hId];
          const w = INDIS[wId];
          spouseG.appendChild(createSpouseLink(h, w));
        }}
      }}
    }});
  }}
}}

function createBezierLink(childId, parentId, cx, cy, px, py, type) {{
  const dx = px - cx;
  const cx1 = cx + dx * 0.45;
  const cx2 = px - dx * 0.45;

  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  // Path starts at Parent (px, py) and ends at Child (cx, cy)
  const d = `M ${{px}} ${{py}} C ${{cx2}} ${{py}}, ${{cx1}} ${{cy}}, ${{cx}} ${{cy}}`;
  path.setAttribute('d', d);
  path.setAttribute('class', `tree-link link-${{type}}`);
  path.setAttribute('id', `link-${{childId}}-${{parentId}}`);
  path.setAttribute('data-child', childId);
  path.setAttribute('data-parent', parentId);
  path.setAttribute('data-type', type);
  path.setAttribute('marker-end', `url(#arrow-${{type}})`);

  return path;
}}

function createSpouseLink(h, w) {{
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('class', 'spouse-group');
  g.setAttribute('id', `spouse-${{h.id}}-${{w.id}}`);

  const CARD_W = 240;
  const CARD_H = 75;

  const x = h.x + CARD_W / 2;
  const y1 = Math.min(h.y, w.y) + CARD_H;
  const y2 = Math.max(h.y, w.y);
  const midY = (y1 + y2) / 2;

  if (Math.abs(h.y - w.y) <= 150) {{
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x);
    line.setAttribute('y2', y2);
    line.setAttribute('class', 'tree-link link-spouse');
    g.appendChild(line);

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', midY + 4);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', '12');
    text.textContent = '💍';
    g.appendChild(text);
  }} else {{
    const rx = h.x + CARD_W + 8;
    const ry1 = h.y + CARD_H / 2;
    const ry2 = w.y + CARD_H / 2;
    const arcMidY = (ry1 + ry2) / 2;
    const curveX = rx + Math.min(45, Math.abs(ry1 - ry2) * 0.15);

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', `M ${{rx}} ${{ry1}} Q ${{curveX}} ${{arcMidY}}, ${{rx}} ${{ry2}}`);
    path.setAttribute('class', 'tree-link link-spouse');
    g.appendChild(path);

    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', curveX + 8);
    text.setAttribute('y', arcMidY + 4);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', '11');
    text.textContent = '💍';
    g.appendChild(text);
  }}

  return g;
}}

// TOGGLES
function toggleSpouseLinks() {{
  showSpouses = !showSpouses;
  const btn = document.getElementById('btnToggleSpouses');
  btn.classList.toggle('active', showSpouses);
  renderSvgLinks();
}}

// INTERACTIVE ANCESTRY HIGHLIGHTING
function highlightLineage(personId) {{
  hoveredPersonId = personId;

  const ancestorIds = new Set();
  const queue = [personId];
  while (queue.length > 0) {{
    const curId = queue.shift();
    ancestorIds.add(curId);
    const p = INDIS[curId];
    if (p) {{
      if (p.father_id) queue.push(p.father_id);
      if (p.mother_id) queue.push(p.mother_id);
      if (p.id === 'I70' && INDIS['I77']) queue.push('I77');
    }}
  }}

  document.querySelectorAll('#cardsLayer .person-card').forEach(c => {{
    const pid = c.id.replace('card-', '');
    if (ancestorIds.has(pid)) {{
      c.classList.add('highlighted');
      c.classList.remove('dimmed');
    }} else {{
      c.classList.remove('highlighted');
      c.classList.add('dimmed');
    }}
  }});

  document.querySelectorAll('.tree-link').forEach(link => {{
    const childId = link.getAttribute('data-child');
    const parentId = link.getAttribute('data-parent');
    if (childId && parentId && ancestorIds.has(childId) && ancestorIds.has(parentId)) {{
      link.classList.add('highlighted');
      link.classList.remove('dimmed');
      link.setAttribute('marker-end', 'url(#arrow-highlight)');
    }} else {{
      link.classList.remove('highlighted');
      link.classList.add('dimmed');
      const type = link.getAttribute('data-type');
      if (type) link.setAttribute('marker-end', `url(#arrow-${{type}})`);
    }}
  }});
}}

function clearHighlight() {{
  hoveredPersonId = null;
  document.querySelectorAll('#cardsLayer .person-card').forEach(c => {{
    c.classList.remove('highlighted', 'dimmed');
  }});
  document.querySelectorAll('.tree-link').forEach(link => {{
    link.classList.remove('highlighted', 'dimmed');
    const type = link.getAttribute('data-type');
    if (type) link.setAttribute('marker-end', `url(#arrow-${{type}})`);
  }});
}}

// ZOOM & PAN LOGIC
function updateTransform() {{
  const canvas = document.getElementById('treeCanvas');
  canvas.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{zoom}})`;

  // Synchronize pinned generation track horizontally
  const track = document.getElementById('pinnedGenTrack');
  if (track) {{
    track.style.transform = `translateX(${{panX}}px) scale(${{zoom}})`;
  }}
}}

function zoomIn() {{
  zoom = Math.min(2.2, zoom + 0.15);
  updateTransform();
}}
function zoomOut() {{
  zoom = Math.max(0.2, zoom - 0.15);
  updateTransform();
}}
function resetZoom() {{
  zoom = 1.0;
  panX = 60;
  panY = 80;
  updateTransform();
}}
function centerOnRoot() {{
  focusGeneration(1);
}}
function fitToScreen() {{
  const viewport = document.getElementById('view-tree');
  const vw = viewport.clientWidth;
  const vh = viewport.clientHeight;
  const treeW = {canvas_w};
  const treeH = {canvas_h};
  zoom = Math.min(vw / treeW, vh / treeH, 0.9);
  panX = (vw - treeW * zoom) / 2;
  panY = 60;
  updateTransform();
}}

function focusPerson(pid) {{
  const p = INDIS[pid];
  if (!p) return;
  if (currentTab !== 'tree') switchTab('tree');

  if (onlyDirectLine && !directAncestorIds.has(pid)) {{
    toggleDirectLine();
  }}

  const viewport = document.getElementById('view-tree');
  const vw = viewport.clientWidth;
  const vh = viewport.clientHeight;

  zoom = 1.0;
  panX = vw / 2 - (p.x + 120);
  panY = vh / 2 - (p.y + 37);
  updateTransform();

  const branchDropdown = document.getElementById('branchSelectDropdown');
  if (branchDropdown) {{
    branchDropdown.value = ['I2', 'I14', 'I10', 'I16', 'I3'].includes(pid) ? pid : '';
  }}

  highlightLineage(pid);
  setTimeout(() => {{
    const card = document.getElementById(`card-${{pid}}`);
    if (card) {{
      card.scrollIntoView?.({{ behavior: 'smooth', block: 'center', inline: 'center' }});
    }}
  }}, 100);
}}

function toggleDirectLine() {{
  onlyDirectLine = !onlyDirectLine;
  const label = onlyDirectLine ? '🎯 Прямая линия (78)' : '🎯 Прямая линия';

  const btn = document.getElementById('btnToggleDirectLine');
  if (btn) {{
    btn.classList.toggle('active', onlyDirectLine);
    btn.innerHTML = label;
  }}
  const btnGen = document.getElementById('btnToggleDirectLineGen');
  if (btnGen) {{
    btnGen.classList.toggle('active', onlyDirectLine);
    btnGen.innerHTML = label;
  }}
  const genCount = document.getElementById('genCountBadge');
  if (genCount) {{
    genCount.textContent = onlyDirectLine ? 'Прямая линия: 78 предков (20 поколений)' : 'Все родственники (197 персон • 20 поколений)';
  }}

  Object.values(INDIS).forEach(p => {{
    const card = document.getElementById(`card-${{p.id}}`);
    if (card) {{
      if (onlyDirectLine && !directAncestorIds.has(p.id)) {{
        card.classList.add('is-hidden-branch');
      }} else {{
        card.classList.remove('is-hidden-branch');
      }}
    }}
  }});

  renderSvgLinks();
  renderGenerations();
}}

function focusGeneration(gen) {{
  gen = parseInt(gen);
  if (!gen || isNaN(gen)) return;

  if (currentTab !== 'tree') switchTab('tree');

  let cards = Object.values(INDIS).filter(p => p.gen === gen);
  if (onlyDirectLine) {{
    const directCards = cards.filter(p => directAncestorIds.has(p.id));
    if (directCards.length > 0) cards = directCards;
  }}
  if (cards.length === 0) return;

  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  cards.forEach(p => {{
    minX = Math.min(minX, p.x);
    maxX = Math.max(maxX, p.x + 246);
    minY = Math.min(minY, p.y);
    maxY = Math.max(maxY, p.y + 78);
  }});

  const centerX = (minX + maxX) / 2;
  const centerY = (minY + maxY) / 2;

  const viewport = document.getElementById('view-tree');
  const vw = viewport.clientWidth;
  const vh = viewport.clientHeight;

  const spanY = Math.max(200, maxY - minY + 140);
  let targetZoom = Math.min(1.0, Math.max(0.55, (vh - 120) / spanY));
  if (vw < 820) {{
    targetZoom = Math.min(0.85, Math.max(0.48, vw / 360));
  }}

  panX = vw / 2 - centerX * targetZoom;
  panY = vh / 2 - centerY * targetZoom;
  zoom = targetZoom;
  updateTransform();

  document.querySelectorAll('.pinned-gen-title').forEach(el => {{
    if (parseInt(el.getAttribute('data-gen')) === gen) {{
      el.classList.add('active-gen');
      setTimeout(() => el.classList.remove('active-gen'), 1800);
    }}
  }});

  const dropdown = document.getElementById('genSelectDropdown');
  if (dropdown) dropdown.value = gen;
}}

/* MOBILE MENU DRAWER & ANCHOR NAVIGATION */
function openMobileMenu() {{
  const drawer = document.getElementById('mobileDrawer');
  const backdrop = document.getElementById('mobileDrawerBackdrop');
  if (drawer) drawer.classList.add('open');
  if (backdrop) backdrop.classList.add('open');
  updateDrawerThemeLabel();
}}

function closeMobileMenu() {{
  const drawer = document.getElementById('mobileDrawer');
  const backdrop = document.getElementById('mobileDrawerBackdrop');
  if (drawer) drawer.classList.remove('open');
  if (backdrop) backdrop.classList.remove('open');
  const results = document.getElementById('drawerSearchResults');
  if (results) results.classList.remove('open');
}}

function toggleMobileMenu() {{
  const drawer = document.getElementById('mobileDrawer');
  if (drawer && drawer.classList.contains('open')) {{
    closeMobileMenu();
  }} else {{
    openMobileMenu();
  }}
}}

function handleDrawerNav(tabId) {{
  switchTab(tabId);
  closeMobileMenu();
}}

function updateDrawerThemeLabel() {{
  const isDark = document.body.getAttribute('data-theme') === 'dark';
  const icon = document.getElementById('drawerThemeIcon');
  const text = document.getElementById('drawerThemeText');
  if (icon) icon.textContent = isDark ? '☀️' : '🌙';
  if (text) text.textContent = isDark ? 'Светлая тема' : 'Темная тема';
}}

function handleDrawerSearch(q) {{
  handleSearch(q);
  const container = document.getElementById('drawerSearchResults');
  if (!container) return;
  q = (q || '').trim().toLowerCase();
  if (q.length < 2) {{
    container.classList.remove('open');
    container.innerHTML = '';
    return;
  }}
  const matches = Object.values(INDIS).filter(p =>
    p.clean_name.toLowerCase().includes(q) ||
    (p.birt_plac && p.birt_plac.toLowerCase().includes(q))
  ).slice(0, 8);

  if (matches.length === 0) {{
    container.innerHTML = '<div style="padding:0.6rem; font-size:0.8rem; color:var(--text-muted); text-align:center;">Никого не найдено</div>';
    container.classList.add('open');
    return;
  }}

  container.innerHTML = matches.map(p => `
    <div onclick="selectDrawerPerson('${{p.id}}')" style="padding:0.55rem 0.75rem; border-bottom:1px solid var(--border-color); cursor:pointer; font-size:0.82rem; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div style="font-weight:600; color:var(--text-main);">${{escapeHtml(p.clean_name)}}</div>
        <div style="font-size:0.72rem; color:var(--text-muted);">Пок. ${{p.gen}} • ${{p.display_birt || '—'}}</div>
      </div>
      <span class="pill-btn" style="font-size:0.7rem; padding:0.15rem 0.4rem;">🎯</span>
    </div>
  `).join('');
  container.classList.add('open');
}}

function selectDrawerPerson(id) {{
  closeMobileMenu();
  switchTab('tree');
  focusPerson(id);
  openModal(id);
}}

function scrollToAnchor(e, targetId) {{
  if (e) e.preventDefault();
  const el = document.getElementById(targetId);
  if (!el) return;
  el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  if (history.pushState) {{
    history.pushState(null, null, '#' + targetId);
  }} else {{
    location.hash = '#' + targetId;
  }}
  const section = el.closest('.view-section');
  if (section) {{
    section.querySelectorAll('.info-bottom-pill').forEach(pill => {{
      pill.classList.toggle('active', pill.getAttribute('href') === '#' + targetId);
    }});
  }}
}}

function setupHashRouting() {{
  const hash = window.location.hash.replace('#', '');
  if (hash) {{
    if (hash.startsWith('info-')) {{
      switchTab('info');
      setTimeout(() => scrollToAnchor(null, hash), 350);
    }} else if (hash === 'books-series' || hash === 'ancient-chronicles' || hash === 'state-archives' || hash === 'ww2-archives' || hash === 'online-databases') {{
      switchTab('sources');
      setTimeout(() => scrollToAnchor(null, hash), 350);
    }}
  }}
}}
window.addEventListener('hashchange', () => {{
  const hash = window.location.hash.replace('#', '');
  if (hash) {{
    if (hash.startsWith('info-')) {{
      switchTab('info');
      scrollToAnchor(null, hash);
    }} else if (hash === 'books-series' || hash === 'ancient-chronicles' || hash === 'state-archives' || hash === 'ww2-archives' || hash === 'online-databases') {{
      switchTab('sources');
      scrollToAnchor(null, hash);
    }}
  }}
}});

function setupCanvasDrag() {{
  const viewport = document.getElementById('view-tree');
  let justDragged = false;
  let dragTimer = null;

  // Mouse Dragging
  viewport.addEventListener('mousedown', e => {{
    if (e.target.closest('.person-card') || e.target.closest('.tree-floating-tools') || e.target.closest('.tree-subbar') || e.target.closest('.tree-legend')) return;
    isDragging = true;
    startX = e.clientX - panX;
    startY = e.clientY - panY;
  }});

  window.addEventListener('mousemove', e => {{
    if (!isDragging) return;
    panX = e.clientX - startX;
    panY = e.clientY - startY;
    justDragged = true;
    updateTransform();
  }});

  window.addEventListener('mouseup', () => {{
    if (isDragging) {{
      isDragging = false;
      clearTimeout(dragTimer);
      dragTimer = setTimeout(() => {{ justDragged = false; }}, 160);
    }}
  }});

  // Mouse Wheel Zoom
  viewport.addEventListener('wheel', e => {{
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    const newZoom = Math.min(2.5, Math.max(0.18, zoom * zoomFactor));

    const rect = viewport.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    panX = mouseX - (mouseX - panX) * (newZoom / zoom);
    panY = mouseY - (mouseY - panY) * (newZoom / zoom);
    zoom = newZoom;
    updateTransform();
  }}, {{ passive: false }});

  // Mobile Touch Support: 1-finger Pan & 2-finger Pinch Zoom
  let touchStartDist = 0;
  let touchStartZoom = zoom;
  let isTouching = false;
  let touchStartX = 0;
  let touchStartY = 0;
  let touchMidX = 0;
  let touchMidY = 0;

  viewport.addEventListener('touchstart', e => {{
    if (e.target.closest('.person-card') || e.target.closest('.tree-floating-tools') || e.target.closest('.tree-subbar') || e.target.closest('.tree-legend') || e.target.closest('.badge-doc-tree')) return;

    if (e.touches.length === 1) {{
      isTouching = true;
      const t = e.touches[0];
      touchStartX = t.clientX - panX;
      touchStartY = t.clientY - panY;
    }} else if (e.touches.length === 2) {{
      isTouching = false;
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      touchStartDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      touchStartZoom = zoom;
      const rect = viewport.getBoundingClientRect();
      touchMidX = (t1.clientX + t2.clientX) / 2 - rect.left;
      touchMidY = (t1.clientY + t2.clientY) / 2 - rect.top;
    }}
  }}, {{ passive: true }});

  viewport.addEventListener('touchmove', e => {{
    if (e.target.closest('.person-card') || e.target.closest('.tree-floating-tools') || e.target.closest('.tree-subbar') || e.target.closest('.tree-legend') || e.target.closest('.badge-doc-tree')) return;

    if (e.touches.length === 1 && isTouching) {{
      const t = e.touches[0];
      const nextPanX = t.clientX - touchStartX;
      const nextPanY = t.clientY - touchStartY;
      if (Math.hypot(nextPanX - panX, nextPanY - panY) > 6) {{
        justDragged = true;
      }}
      panX = nextPanX;
      panY = nextPanY;
      updateTransform();
    }} else if (e.touches.length === 2 && touchStartDist > 0) {{
      e.preventDefault();
      justDragged = true;
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const currentDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      const scale = currentDist / touchStartDist;
      const newZoom = Math.min(2.5, Math.max(0.18, touchStartZoom * scale));

      panX = touchMidX - (touchMidX - panX) * (newZoom / zoom);
      panY = touchMidY - (touchMidY - panY) * (newZoom / zoom);
      zoom = newZoom;
      updateTransform();
    }}
  }}, {{ passive: false }});

  viewport.addEventListener('touchend', e => {{
    if (e.touches.length === 0) {{
      isTouching = false;
      touchStartDist = 0;
      clearTimeout(dragTimer);
      dragTimer = setTimeout(() => {{ justDragged = false; }}, 160);
    }} else if (e.touches.length === 1) {{
      isTouching = true;
      const t = e.touches[0];
      touchStartX = t.clientX - panX;
      touchStartY = t.clientY - panY;
    }}
  }});

  viewport.addEventListener('touchcancel', () => {{
    isTouching = false;
    touchStartDist = 0;
    justDragged = false;
  }});

  window.wasCanvasDragged = () => justDragged;
}}


// ============================================================================
// ARCHIVE GALLERY & DOC VIEWER CONTROLLER
// ============================================================================
let currentDocIndex = 0;
let currentDocList = DOCS;
let docZoom = 1;
let docPanX = 0;
let docPanY = 0;
let isDocDragging = false;
let docStartX = 0, docStartY = 0;
let currentArchiveFilter = 'all';
let currentArchiveQuery = '';

function renderArchiveGrid() {{
  const container = document.getElementById('archiveGrid');
  if (!container) return;
  container.innerHTML = '';
  
  let list = DOCS;
  if (currentArchiveFilter !== 'all') {{
    list = list.filter(d => d.category === currentArchiveFilter);
  }}
  if (currentArchiveQuery) {{
    const q = currentArchiveQuery.toLowerCase();
    list = list.filter(d => 
      (d.title && d.title.toLowerCase().includes(q)) || 
      (d.desc && d.desc.toLowerCase().includes(q)) ||
      (d.archive && d.archive.toLowerCase().includes(q)) ||
      (d.personName && d.personName.toLowerCase().includes(q))
    );
  }}

  if (list.length === 0) {{
    container.innerHTML = '<div style="grid-column: 1 / -1; text-align:center; padding:3rem; color:var(--text-muted); font-size:1rem;">Документы не найдены по запросу</div>';
    return;
  }}

  list.forEach(doc => {{
    const card = document.createElement('div');
    card.className = 'doc-card';
    card.onclick = () => openDocViewer(DOCS.indexOf(doc), DOCS);
    
    card.innerHTML = `
      <div class="doc-card-thumb-wrap">
        <img src="${{escapeHtml(doc.thumb)}}" alt="${{escapeHtml(doc.title)}}" loading="lazy" />
        <span class="doc-badge-overlay" style="border-color:${{doc.badgeColor || '#2563eb'}}66; color:${{doc.badgeColor || '#fff'}};">${{escapeHtml(doc.badge || doc.categoryLabel)}}</span>
        <span class="doc-zoom-hint">🔍 Смотреть</span>
      </div>
      <div class="doc-card-content">
        <div>
          <div class="doc-card-title">${{escapeHtml(doc.title)}}</div>
          <div class="doc-card-meta">
            ${{doc.personName ? `<strong>${{escapeHtml(doc.personName)}}</strong> • ` : ''}}
            <span>${{escapeHtml(doc.date || '')}}</span><br/>
            <span>🏛️ ${{escapeHtml(doc.archive)}}</span>
          </div>
          <div class="doc-card-desc">${{escapeHtml(doc.desc)}}</div>
        </div>
        <div class="doc-card-actions" onclick="event.stopPropagation()">
          <button class="pill-btn active" onclick="openDocViewer(DOCS.indexOf(doc), DOCS)" style="flex:1; font-size:0.76rem; justify-content:center;">🔍 Смотреть скан</button>
          <button class="pill-btn" onclick="openFullscreenScan(DOCS[${{DOCS.indexOf(doc)}}])" style="font-size:0.76rem;" title="Открыть скан на весь экран с возможностью зума">🔍 ↗</button>
          ${{doc.personId ? `<button class="pill-btn" onclick="focusPerson('${{doc.personId}}'); switchTab('tree');" style="font-size:0.76rem;" title="Найти персону на древе">🎯</button>` : ''}}
        </div>
      </div>
    `;
    container.appendChild(card);
  }});
}}

function filterArchiveCategory(cat) {{
  currentArchiveFilter = cat;
  document.querySelectorAll('#archiveFilterPills button').forEach(b => {{
    b.classList.remove('active');
  }});
  if (event && event.target) {{
    event.target.classList.add('active');
  }}
  renderArchiveGrid();
}}

function handleArchiveSearch(q) {{
  currentArchiveQuery = q.trim();
  renderArchiveGrid();
}}

function openDocViewer(index, customList) {{
  if (customList && customList.length) currentDocList = customList;
  else currentDocList = DOCS;
  
  if (index < 0) index = 0;
  if (index >= currentDocList.length) index = currentDocList.length - 1;
  currentDocIndex = index;
  
  const doc = currentDocList[currentDocIndex];
  if (!doc) return;

  document.getElementById('docViewerTitle').textContent = doc.title;
  const badgeEl = document.getElementById('docViewerBadge');
  badgeEl.textContent = doc.badge || doc.categoryLabel;
  badgeEl.style.background = (doc.badgeColor || '#2563eb') + '22';
  badgeEl.style.color = doc.badgeColor || '#2563eb';
  badgeEl.style.borderColor = (doc.badgeColor || '#2563eb') + '66';
  
  document.getElementById('docViewerPerson').textContent = doc.personName ? `• ${{doc.personName}}` : '';
  document.getElementById('docViewerArchive').textContent = `${{doc.archive}}${{doc.date ? ' • ' + doc.date : ''}}`;
  document.getElementById('docViewerDesc').textContent = doc.desc;
  document.getElementById('docViewerCounter').textContent = `${{currentDocIndex + 1}} из ${{currentDocList.length}}`;
  
  const img = document.getElementById('docViewerImg');
  img.src = doc.file;
  
  const dlBtn = document.getElementById('docViewerDownloadBtn');
  if (dlBtn) dlBtn.href = doc.file;

  docResetZoom();
  document.getElementById('docViewerModal').classList.add('open');
  
  document.getElementById('docNavPrev').style.display = currentDocIndex > 0 ? 'flex' : 'none';
  document.getElementById('docNavNext').style.display = currentDocIndex < currentDocList.length - 1 ? 'flex' : 'none';
}}

function openCurrentDocInNewTab() {{
  const doc = currentDocList[currentDocIndex];
  if (doc) {{
    openFullscreenScan(doc);
  }}
}}

// ============================================================================
// FULLSCREEN SCAN LIGHTBOX CONTROLLER
// ============================================================================
let fsZoom = 1.0;
let fsPanX = 0;
let fsPanY = 0;
let isFsDragging = false;
let fsStartX = 0;
let fsStartY = 0;
let fsPinchDistStart = 0;
let fsPinchZoomStart = 1.0;

function openFullscreenScan(docOrFile, title, meta) {{
  let file = '';
  let titleText = 'Оригинал документа';
  let metaText = '';

  if (typeof docOrFile === 'object' && docOrFile !== null) {{
    file = docOrFile.file || '';
    titleText = docOrFile.title || 'Оригинал документа';
    const parts = [];
    if (docOrFile.personName) parts.push(docOrFile.personName);
    if (docOrFile.date) parts.push(docOrFile.date);
    if (docOrFile.archive) parts.push(`🏛️ ${{docOrFile.archive}}`);
    metaText = parts.join(' • ');
  }} else if (typeof docOrFile === 'string' && docOrFile.length > 0) {{
    file = docOrFile;
    if (title) titleText = title;
    if (meta) metaText = meta;
  }} else {{
    const cur = currentDocList[currentDocIndex];
    if (cur) {{
      file = cur.file;
      titleText = cur.title;
      const parts = [];
      if (cur.personName) parts.push(cur.personName);
      if (cur.date) parts.push(cur.date);
      if (cur.archive) parts.push(`🏛️ ${{cur.archive}}`);
      metaText = parts.join(' • ');
    }}
  }}

  if (!file) return;

  const img = document.getElementById('fsScanImg');
  if (img) img.src = file;

  const titleEl = document.getElementById('fsScanTitle');
  if (titleEl) titleEl.textContent = titleText;

  const metaEl = document.getElementById('fsScanMeta');
  if (metaEl) metaEl.textContent = metaText;

  fsResetZoom();
  const modal = document.getElementById('fsScanModal');
  if (modal) modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}}

function closeFsScan() {{
  const modal = document.getElementById('fsScanModal');
  if (modal) modal.classList.remove('open');
  const isDocOpen = document.getElementById('docViewerModal') && document.getElementById('docViewerModal').classList.contains('open');
  const isPersonOpen = document.getElementById('personModal') && document.getElementById('personModal').classList.contains('open');
  if (!isDocOpen && !isPersonOpen) {{
    document.body.style.overflow = '';
  }}
}}

function closeFsScanOnOverlay(e) {{
  if (e.target.id === 'fsScanModal' || e.target.id === 'fsScanViewport') {{
    closeFsScan();
  }}
}}

function fsZoomIn() {{
  fsZoom = Math.min(fsZoom * 1.35, 6.0);
  updateFsTransform();
}}

function fsZoomOut() {{
  fsZoom = Math.max(fsZoom / 1.35, 0.4);
  updateFsTransform();
}}

function fsResetZoom() {{
  fsZoom = 1.0;
  fsPanX = 0;
  fsPanY = 0;
  updateFsTransform();
}}

function updateFsTransform() {{
  const cont = document.getElementById('fsScanImgContainer');
  if (cont) {{
    cont.style.transform = `translate(${{fsPanX}}px, ${{fsPanY}}px) scale(${{fsZoom}})`;
  }}
  const lbl = document.getElementById('fsZoomLabel');
  if (lbl) {{
    lbl.textContent = `${{Math.round(fsZoom * 100)}}%`;
  }}
}}

function setupFsScanEvents() {{
  const vp = document.getElementById('fsScanViewport');
  if (!vp) return;

  vp.addEventListener('mousedown', (e) => {{
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
    isFsDragging = true;
    fsStartX = e.clientX - fsPanX;
    fsStartY = e.clientY - fsPanY;
    vp.classList.add('dragging');
  }});

  window.addEventListener('mousemove', (e) => {{
    if (!isFsDragging) return;
    fsPanX = e.clientX - fsStartX;
    fsPanY = e.clientY - fsStartY;
    updateFsTransform();
  }});

  window.addEventListener('mouseup', () => {{
    if (isFsDragging) {{
      isFsDragging = false;
      vp.classList.remove('dragging');
    }}
  }});

  vp.addEventListener('wheel', (e) => {{
    e.preventDefault();
    if (e.deltaY < 0) {{
      fsZoomIn();
    }} else {{
      fsZoomOut();
    }}
  }}, {{ passive: false }});

  vp.addEventListener('dblclick', (e) => {{
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
    if (fsZoom > 1.2) {{
      fsResetZoom();
    }} else {{
      fsZoom = 2.4;
      updateFsTransform();
    }}
  }});

  vp.addEventListener('touchstart', (e) => {{
    if (e.touches.length === 1) {{
      isFsDragging = true;
      fsStartX = e.touches[0].clientX - fsPanX;
      fsStartY = e.touches[0].clientY - fsPanY;
    }} else if (e.touches.length === 2) {{
      isFsDragging = false;
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      fsPinchDistStart = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      fsPinchZoomStart = fsZoom;
    }}
  }}, {{ passive: true }});

  vp.addEventListener('touchmove', (e) => {{
    if (e.touches.length === 1 && isFsDragging) {{
      fsPanX = e.touches[0].clientX - fsStartX;
      fsPanY = e.touches[0].clientY - fsStartY;
      updateFsTransform();
    }} else if (e.touches.length === 2 && fsPinchDistStart > 0) {{
      const t1 = e.touches[0];
      const t2 = e.touches[1];
      const dist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
      const factor = dist / fsPinchDistStart;
      fsZoom = Math.max(0.4, Math.min(6.0, fsPinchZoomStart * factor));
      updateFsTransform();
    }}
  }}, {{ passive: true }});

  vp.addEventListener('touchend', (e) => {{
    if (e.touches.length === 0) {{
      isFsDragging = false;
      fsPinchDistStart = 0;
    }} else if (e.touches.length === 1) {{
      isFsDragging = true;
      fsStartX = e.touches[0].clientX - fsPanX;
      fsStartY = e.touches[0].clientY - fsPanY;
      fsPinchDistStart = 0;
    }}
  }}, {{ passive: true }});
}}

function openDocViewerById(docId) {{
  const idx = DOCS.findIndex(d => d.id === docId);
  if (idx !== -1) {{
    openDocViewer(idx, DOCS);
  }}
}}

function openDocViewerByFile(filePath) {{
  const idx = DOCS.findIndex(d => d.file === filePath || d.file.endsWith(filePath));
  if (idx !== -1) {{
    openDocViewer(idx, DOCS);
  }}
}}

function closeDocViewer() {{
  document.getElementById('docViewerModal').classList.remove('open');
}}

function closeDocViewerOnOverlay(e) {{
  if (e.target.id === 'docViewerModal') closeDocViewer();
}}

function docNext() {{
  if (currentDocIndex < currentDocList.length - 1) {{
    openDocViewer(currentDocIndex + 1, currentDocList);
  }}
}}

function docPrev() {{
  if (currentDocIndex > 0) {{
    openDocViewer(currentDocIndex - 1, currentDocList);
  }}
}}

function docZoomIn() {{
  docZoom = Math.min(docZoom * 1.3, 4.0);
  updateDocTransform();
}}

function docZoomOut() {{
  docZoom = Math.max(docZoom / 1.3, 0.4);
  updateDocTransform();
}}

function docResetZoom() {{
  docZoom = 1;
  docPanX = 0;
  docPanY = 0;
  updateDocTransform();
}}

function updateDocTransform() {{
  const img = document.getElementById('docViewerImg');
  img.style.transform = `translate(${{docPanX}}px, ${{docPanY}}px) scale(${{docZoom}})`;
}}

let docDidDrag = false;
let docClickStartX = 0;
let docClickStartY = 0;

function setupDocViewerEvents() {{
  const vp = document.getElementById('docViewerViewport');
  if (!vp) return;

  vp.addEventListener('mousedown', (e) => {{
    if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
    isDocDragging = true;
    docDidDrag = false;
    docClickStartX = e.clientX;
    docClickStartY = e.clientY;
    docStartX = e.clientX - docPanX;
    docStartY = e.clientY - docPanY;
    document.getElementById('docImgWrapper').classList.add('dragging');
  }});

  window.addEventListener('mousemove', (e) => {{
    if (!isDocDragging) return;
    if (Math.abs(e.clientX - docClickStartX) > 6 || Math.abs(e.clientY - docClickStartY) > 6) {{
      docDidDrag = true;
    }}
    docPanX = e.clientX - docStartX;
    docPanY = e.clientY - docStartY;
    updateDocTransform();
  }});

  window.addEventListener('mouseup', () => {{
    if (isDocDragging) {{
      isDocDragging = false;
      const wr = document.getElementById('docImgWrapper');
      if (wr) wr.classList.remove('dragging');
    }}
  }});

  const wr = document.getElementById('docImgWrapper');
  if (wr) {{
    wr.addEventListener('click', (e) => {{
      if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
      if (!docDidDrag) {{
        openCurrentDocInNewTab();
      }}
    }});
  }}

  vp.addEventListener('wheel', (e) => {{
    e.preventDefault();
    if (e.deltaY < 0) docZoomIn();
    else docZoomOut();
  }}, {{ passive: false }});
}}

// MODAL PROFILE
function openModal(pid) {{
  const p = INDIS[pid];
  if (!p) return;

  const personDocs = getPersonDocs(pid);
  const srcInfo = getPersonSourceInfo(p);
  let docBtn = '';
  if (personDocs.length > 0) {{
    const firstDocIdx = DOCS.indexOf(personDocs[0]);
    docBtn = `<button class="pill-btn" onclick="openDocViewer(${{firstDocIdx}}, getPersonDocs('${{p.id}}'))" style="background:#2563eb; color:#fff; border-color:#2563eb; font-size:0.8rem; font-weight:600;">🏛️ Смотреть сканы (${{personDocs.length}})</button>`;
  }}

  document.getElementById('modalName').textContent = p.clean_name;
  document.getElementById('modalSubtitle').textContent = `Поколение ${{p.gen}} • ${{p.branch}}`;

  const sexText = p.sex === 'M' ? 'Мужской ♂' : 'Женский ♀';
  const dates = p.display_birt ? `${{p.display_birt}}${{p.display_deat ? ' — ' + p.display_deat : ''}}` : (p.display_deat ? `ум. ${{p.display_deat}}` : 'не указано');

  let html = `
    <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.75rem;">
      <button class="pill-btn active" onclick="focusPerson('${{p.id}}'); closeModal();" style="font-size:0.8rem;">🎯 Показать на древе</button>
      ${{docBtn}}
    </div>

    <div class="detail-group">
      <h3>Основная информация</h3>
      <div class="detail-item"><strong>Пол:</strong> ${{sexText}}</div>
      <div class="detail-item"><strong>Даты:</strong> ${{dates}}</div>
      ${{p.birt_plac ? `<div class="detail-item"><strong>Место рождения:</strong> 📍 ${{escapeHtml(p.birt_plac)}}</div>` : ''}}
      <div class="detail-item"><strong>Ветвь:</strong> <span style="color:${{p.branch_color}}; font-weight:700;">${{p.branch}}</span></div>
    </div>
  `;

  if (srcInfo && srcInfo.type === 'text') {{
    html += `
      <div class="detail-group" style="background:var(--bg-primary); border-left:3px solid var(--accent); border-radius:6px; padding:0.65rem 0.85rem;">
        <div style="font-weight:700; font-size:0.82rem; color:var(--text-main); margin-bottom:0.25rem;">📚 Источник сведений:</div>
        <div style="font-size:0.8rem; line-height:1.45; color:var(--text-muted);">
          ${{escapeHtml(srcInfo.text)}}
        </div>
      </div>
    `;
  }}

  if (p.id === 'I19' || p.id === 'I67' || p.id === 'I68' || p.id === 'I25' || p.id === 'I23' || p.id === 'I21') {{
    html += `
      <div class="detail-group" style="background: linear-gradient(135deg, rgba(220,38,38,0.07), rgba(245,158,11,0.07)); border: 1.5px solid rgba(220,38,38,0.25); border-radius:8px; padding:0.75rem 0.85rem;">
        <div style="display:flex; align-items:center; gap:0.45rem; margin-bottom:0.45rem;">
          <span style="font-size:1.15rem;">🎖️</span>
          <h3 style="margin:0; color:#b91c1c; font-size:0.92rem;">${{p.id === 'I25' ? 'Ветеран двух мировых войн (ПМВ и ВОВ)' : (p.id === 'I21' ? 'Младший лейтенант ВОВ • Кавалер Ордена Отечественной войны I ст.' : (p.id === 'I68' || p.id === 'I23' ? 'Участник Великой Отечественной войны' : 'Герой Великой Отечественной войны'))}}</h3>
        </div>
        <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
          ${{p.id === 'I25' ? `
            <div style="margin-bottom:0.45rem; padding-bottom:0.45rem; border-bottom:1px dashed rgba(220,38,38,0.25);">
              <div style="font-weight:700; color:#991b1b; margin-bottom:0.15rem;">⚔️ Первая мировая война (1914–1918):</div>
              <div><strong>Звание:</strong> Унтер-офицер (ранее ефрейтор) Русской императорской армии</div>
              <div><strong>Воинская часть:</strong> 181-й пехотный Остроленский полк (46-я пехотная дивизия, 21-й армейский корпус)</div>
              <div><strong>Бои и пленение:</strong> Участник Галицийской битвы и Краковской операции. В боях под Краковом (Ковали, Костелец, Циборовице) 8–13 ноября 1914 г. пропал без вести (РГВИА ф. 16196, оп. 1, д. 346, док. 31904). Пленен 21.12.1914 г., с 15.01.1915 г. содержался в лагере военнопленных Миловиц (Milowitz, Австро-Венгрия, ныне Чехия; РГВИА, ящик 6292-К). Вернулся на родину в Коми край.</div>
            </div>
            <div>
              <div style="font-weight:700; color:#991b1b; margin-bottom:0.15rem;">🛡️ Великая Отечественная война (1941–1945):</div>
              <div><strong>Звание и должность:</strong> Старший артиллерист 7-й роты 2-го стрелкового батальона 34-го запасного стрелкового полка</div>
              <div><strong>Призыв:</strong> Мобилизован в возрасте 53 лет (1943 г.)</div>
              <div><strong>Музейный документ:</strong> Подлинная Красноармейская книжка от 13.06.1943 г. («Годен к … 7.8.44»). Хранится в Айкинском центральном музее Усть-Вымского района Коми (КП 8347, рег. № 21112145).</div>
            </div>
          ` : p.id === 'I21' ? `
            <div><strong>Родство:</strong> Прапрадед Николая, отец Зинаиды Михайловны Туркиной (Шехониной), муж Марии Степановны Сюткиной. Родился и жил в селе Лойма Прилузского района Коми АССР.</div>
            <div><strong>Воинское звание:</strong> Младший лейтенант (офицер РККА)</div>
            <div><strong>Призыв:</strong> Мобилизован Прилузским РВК Коми АССР в июле 1941 года.</div>
            <div><strong>Воинская часть:</strong> 995-й стрелковый полк 263-й стрелковой дивизии (Карельский фронт).</div>
            <div><strong>Боевой путь и ранение:</strong> Участвовал в ожесточенных оборонительных и наступательных боях 1941–1942 гг. на Карельском фронте (Масельгское направление, Кировская железная дорога). В боях получил тяжелое боевое ранение. Проходил лечение в 25-м отдельном медико-санитарном батальоне (25 медсб 263 сд), затем эвакуирован в тыловые эвакогоспитали: ЭГ 1438 / 1439 и ЭГ 2513.</div>
            <div><strong>Демобилизация:</strong> Демобилизован по ранению в январе 1943 года (выбыл из госпиталя 25.01.1943 г.). Вернулся на родину в село Лойма.</div>
            <div><strong>Награды:</strong> <strong>Орден Отечественной войны I степени</strong> (Указ Президиума Верховного Совета СССР / Приказ МО СССР № 89 от 06.04.1985 г., ЦАМО РФ шкаф 62, ящик 2; I степень присвоена за боевое ранение на фронте).</div>
            <div><strong>Кончина:</strong> Скончался в ноябре 1988 года в возрасте 79 лет в с. Лойма.</div>
            <div><strong>Архивные первоисточники:</strong> Филиал ЦАМО РФ (военно-медицинских документов, г. Санкт-Петербург), Картотека общего учета (ящик 096-26), фонд «Свидетельства о болезни» (ящик ЭГ 2513); ЦАМО РФ (Юбилейная картотека, шкаф 62, ящик 2); Книга Памяти Республики Коми, том 5, стр. 612.</div>
          ` : p.id === 'I23' ? `
            <div><strong>Родство:</strong> Прапрадед Николая, отец Евгения Александровича Шуктомова, муж Серафимы Афанасьевны Полещиковой. Родился в д. Ероздино Усть-Вымского района.</div>
            <div><strong>Воинское звание:</strong> Рядовой (стрелок)</div>
            <div><strong>Призыв:</strong> Мобилизован Усть-Вымским РВК Коми АССР в декабре 1941 года.</div>
            <div><strong>Воинская часть:</strong> 34-й запасной стрелковый полк 29-й запасной стрелковой дивизии (2-й батальон, 5-я стрелковая рота, запись № 3526).</div>
            <div><strong>Боевой путь:</strong> Проходил подготовку на сборном пункте 34 зсп в конце 1941 — начале 1942 г. 18 января 1942 года с маршевой командой № 43 направлен на фронт в действующую армию. Демобилизован в июле 1942 года. Прожил трудовую жизнь в Коми крае, скончался в сентябре 1970 года.</div>
            <div><strong>Увековечение:</strong> Книга Памяти Республики Коми, том 6, стр. 705; Центральный архив Министерства обороны РФ (фонд 8312, опись 37579с, дело 3, кадр 38).</div>
          ` : p.id === 'I19' ? `
            <div><strong>Звание:</strong> Гвардии старший сержант</div>
            <div><strong>Части:</strong> 18 гв. мехбригада 9 гв. мехкорпуса (6-я гвардейская танковая армия); 45 мехбригада 5 мехкорпуса</div>
            <div><strong>Должность:</strong> Командир расчета 82-мм минометов</div>
            <div><strong>Боевой путь в Европе:</strong> Брянский, Юго-Западный (оборона Сталинграда), Западный, 1-й и 2-й Украинские фронты, освобождение Румынии, Венгрии, Австрии, штурм Вены, Пражская операция.</div>
            <div><strong>Журнал боевых действий (ЖБД 45 мбр, 03.06.1944 г.):</strong> В подлинном ЖБД зафиксирован подвиг у высоты 137.0 (Стынка): <em>«В 16.30 3.6.44 пр-к силами до полка пехоты при поддержке 10 танков снова перешел в атаку... Исход этого боя в основном был решен нашими минометами, которые своим метким огнем сумели быстро отсечь пехоту пр-ка от танков и нанести ей значительные потери»</em>. За этот бой награжден медалью «За боевые заслуги».</div>
            <div><strong>Маньчжурская стратегическая операция (август-сентябрь 1945 г.):</strong> Забайкальский фронт. Совершил 800-км марш через пустыню Гоби и хребет Большой Хинган, освобождал Мукден (Шэньян), разгром Квантунской армии.</div>
            <div><strong>Награды:</strong> Орден Славы III ст. (1945), Медаль «За боевые заслуги» (1944), Медаль «За победу над Японией» (1945), Медаль «За взятие Вены» (1945), Медаль «За оборону Сталинграда» (1942), Медаль «За победу над Германией» (1945), Орден Отечественной войны II ст. (1985), нагрудный знак «Отличный минометчик». Благодарность ВГК И.В. Сталина (приказ № 372). Присвоение бригаде почетного наименования «Хинганская».</div>
          ` : p.id === 'I68' ? `
            <div><strong>Родство:</strong> Родной младший брат Михаила Николаевича Туркина, сын Николая Алексеевича Туркина и Павлы Ивановны Сизевой. Родился в д. Сюлатуй Коквицкого с/с.</div>
            <div><strong>Призыв:</strong> Мобилизован в июне 1941 года Сыктывкарским ГВК Коми АССР.</div>
            <div><strong>Увековечение:</strong> Книга Памяти Республики Коми, том 6.</div>
          ` : `
            <div><strong>Звание:</strong> Старший сержант</div>
            <div><strong>Части:</strong> 951 сп 265 сд (3-я ударная армия, 1-й Белорусский фронт)</div>
            <div><strong>Должность:</strong> Командир минометного расчета 1-й минроты</div>
            <div><strong>Боевой путь:</strong> Ленинградский фронт, Карельский перешеек, Прибалтика, Варшава, взятие Берлина.</div>
            <div><strong>Награды:</strong> Орден Красной Звезды (1945), Орден Славы III ст. (1944), Медаль «За отвагу» (1944), Медали «За взятие Берлина» (1945), «За освобождение Варшавы» (1945), «За победу над Германией» (1945).</div>
          `}}
        </div>
      </div>
    `;
  }}

  if (p.id === 'I33') {{
    html += `
      <div class="detail-group" style="background: linear-gradient(135deg, rgba(139,92,246,0.07), rgba(239,68,68,0.07)); border: 1.5px solid rgba(139,92,246,0.25); border-radius:8px; padding:0.75rem 0.85rem;">
        <div style="display:flex; align-items:center; gap:0.45rem; margin-bottom:0.45rem;">
          <span style="font-size:1.15rem;">📜</span>
          <h3 style="margin:0; color:#7c3aed; font-size:0.92rem;">Жертва политических репрессий (раскулачивание)</h3>
        </div>
        <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
          <div><strong>Статус:</strong> Крестьянин-единоличник деревни Вотинская Лоемского сельсовета.</div>
          <div><strong>Репрессии:</strong> В 1930 г. был раскулачен и лишён избирательных прав по классовому признаку. Погиб/умер в 1933 г. Реабилитирован.</div>
          <div><strong>Источники:</strong> Мартиролог жертв политических репрессий РК «Покаяние» (т. 8/4), база данных «Открытый список» по материалам ИЦ МВД Республики Коми.</div>
        </div>
      </div>
    `;
  }}

  if (p.id === 'I314' || p.id === 'I315') {{
    const ageText = p.id === 'I314' ? '39 лет' : '22 года';
    html += `
      <div class="detail-group" style="background: linear-gradient(135deg, rgba(220,38,38,0.07), rgba(245,158,11,0.07)); border: 1.5px solid rgba(220,38,38,0.25); border-radius:8px; padding:0.75rem 0.85rem;">
        <div style="display:flex; align-items:center; gap:0.45rem; margin-bottom:0.45rem;">
          <span style="font-size:1.15rem;">🎖️</span>
          <h3 style="margin:0; color:#b91c1c; font-size:0.92rem;">Участник Великой Отечественной войны (погиб на фронте)</h3>
        </div>
        <div style="font-size:0.82rem; line-height:1.5; color:var(--text-main);">
          <div><strong>Родство:</strong> Родной брат прабабушки Марии Степановны Сюткиной (Шехониной), сын Степана Петровича и Екатерины Васильевны Сюткиных. Родился в с. Лойма.</div>
          <div><strong>Воинский подвиг:</strong> Призван на фронт Великой Отечественной войны. Погиб в боях за Родину в 1942 году (в возрасте ${{ageText}}).</div>
          <div><strong>Источник:</strong> Личный семейный архив (родословное древо Олега Лычковского, с. Лойма).</div>
        </div>
      </div>
    `;
  }}



  if (personDocs.length > 0) {{
    let pdfLink = '';
    let archiveTitle = `📑 Архивные документы (${{personDocs.length}})`;
    if (p.id === 'I19') {{
      pdfLink = '<a href="pdf_документы/Туркин Михаил Николаевич 1906.pdf" target="_blank" style="font-size:0.75rem; color:var(--accent); text-decoration:none; font-weight:600;">📥 PDF-альбом (19 стр.)</a>';
      archiveTitle = `📑 Архивные сканы ЦАМО РФ (${{personDocs.length}} документов)`;
    }} else if (p.id === 'I67') {{
      pdfLink = '<a href="pdf_документы/Зиновьев Владимир Семенович 1925.pdf" target="_blank" style="font-size:0.75rem; color:var(--accent); text-decoration:none; font-weight:600;">📥 PDF-альбом (19 стр.)</a>';
      archiveTitle = `📑 Архивные сканы ЦАМО РФ (${{personDocs.length}} документов)`;
    }} else if (p.id === 'I25') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">РГВИА и Айкинский музей</span>';
      archiveTitle = `🏛️ Подлинные архивные сканы ПМВ и ВОВ (${{personDocs.length}})`;
    }} else if (p.id === 'I23') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">ЦАМО РФ и Книга Памяти РК</span>';
      archiveTitle = `📑 Архивные документы ВОВ (${{personDocs.length}})`;
    }} else if (p.id === 'I21') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">ЦАМО РФ, Филиал ВМД и Книга Памяти РК</span>';
      archiveTitle = `📑 Архивные документы и картотеки ВОВ (${{personDocs.length}})`;
    }} else if (p.id === 'I248') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--text-muted); font-weight:600;">ГАВО ф. 388, оп. 9, д. 201</span>';
      archiveTitle = `🏛️ Ревизская сказка 1816 г. (семья 171) (${{personDocs.length}})`;
    }} else if (['I75','I76','I77','I78','I79','I80','I81','I82'].includes(p.id)) {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--accent); font-weight:600;">МКАУ ВЦА ф. 363, оп. 1, д. 2372, л. 472</span>';
      archiveTitle = `🏛️ Исповедная роспись 1773 г. (двор 167) (${{personDocs.length}})`;
    }} else if (p.id === 'I74') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--accent); font-weight:600;">РГАДА (Москва), ф. 1209, оп. 1, д. 1080, Л. 35</span>';
      archiveTitle = `🏛️ Переписная книга Яренского уезда 1646 г. (${{personDocs.length}})`;
    }} else if (p.id === 'I73' || p.id === 'I83') {{
      pdfLink = '<span style="font-size:0.75rem; color:var(--accent); font-weight:600;">РГАДА, ф. 1209, д. 1080 (1646 г.) и д. 1081 (1678 г.)</span>';
      archiveTitle = `🏛️ Переписные книги XVII века (${{personDocs.length}})`;
    }} else if (['I71','I104','I72','I84','I85','I86','I87','I88','I89','I90','I91','I92','I93','I94','I95','I96','I97','I98','I99','I100','I101','I102','I103'].includes(p.id)) {{
      pdfLink = '<a href="pdf_документы/КОМИ КРАЙ В НАЧАЛЕ XVIII ВЕКА переписная книга яренского уезда 1710 года.pdf" target="_blank" style="font-size:0.75rem; color:var(--accent); text-decoration:none; font-weight:600;">📥 Академическое издание 1710 г. (PDF, 168 стр.)</a>';
      archiveTitle = `🏛️ Первоисточники переписи 1710 г. (${{personDocs.length}})`;
    }}

    const firstDocIdx = DOCS.indexOf(personDocs[0]);
    html += `
      <div class="detail-group" style="background:rgba(37,99,235,0.04); border:1.5px solid rgba(37,99,235,0.25); border-radius:8px; padding:0.75rem 0.85rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; flex-wrap:wrap; gap:0.35rem;">
          <h3 style="margin:0; font-size:0.92rem;">${{archiveTitle}}</h3>
          ${{pdfLink}}
        </div>
        <div class="person-docs-mini-grid">
          ${{personDocs.map(d => `
            <div class="person-doc-thumb-item" onclick="openDocViewerById('${{d.id}}')" title="${{escapeHtml(d.title)}}">
              <img src="${{escapeHtml(d.thumb)}}" alt="${{escapeHtml(d.title)}}" loading="lazy" />
              <span class="thumb-label">${{escapeHtml(d.badge || d.title)}}</span>
            </div>
          `).join('')}}
        </div>
        <div style="margin-top:0.5rem;">
          <button class="pill-btn active" onclick="openDocViewer(${{firstDocIdx}}, getPersonDocs('${{p.id}}'))" style="font-size:0.76rem; width:100%; justify-content:center;">🔍 Смотреть все (${{personDocs.length}})</button>
        </div>
      </div>
    `;
  }}

  // Parents
  if (p.father_id || p.mother_id) {{
    html += `<div class="detail-group"><h3>Родители</h3><div>`;
    if (p.father_id && INDIS[p.father_id]) {{
      html += `<a class="link-badge" onclick="openModal('${{p.father_id}}')">👨 Отец: ${{escapeHtml(INDIS[p.father_id].clean_name)}}</a>`;
    }}
    if (p.mother_id && INDIS[p.mother_id]) {{
      html += `<a class="link-badge" onclick="openModal('${{p.mother_id}}')">👩 Мать: ${{escapeHtml(INDIS[p.mother_id].clean_name)}}</a>`;
    }}
    html += `</div></div>`;
  }}

  // Spouses
  if (p.spouses && p.spouses.length > 0) {{
    html += `<div class="detail-group"><h3>Брак / Супруг(а)</h3><div>`;
    p.spouses.forEach(s => {{
      if (INDIS[s.id]) {{
        const marr = s.marr_date ? ` (брак: ${{s.marr_date}})` : '';
        html += `<a class="link-badge" onclick="openModal('${{s.id}}')">💍 ${{escapeHtml(INDIS[s.id].clean_name)}}${{marr}}</a>`;
      }}
    }});
    html += `</div></div>`;
  }}

  // Children
  if (p.children_ids && p.children_ids.length > 0) {{
    html += `<div class="detail-group"><h3>Дети (${{p.children_ids.length}})</h3><div>`;
    p.children_ids.forEach(cid => {{
      if (INDIS[cid]) {{
        html += `<a class="link-badge" onclick="openModal('${{cid}}')">👶 ${{escapeHtml(INDIS[cid].clean_name)}}</a>`;
      }}
    }});
    html += `</div></div>`;
  }}

  // Siblings
  if (p.siblings_ids && p.siblings_ids.length > 0) {{
    html += `<div class="detail-group"><h3>Братья и сёстры</h3><div>`;
    p.siblings_ids.forEach(sid => {{
      if (INDIS[sid]) {{
        html += `<a class="link-badge" onclick="openModal('${{sid}}')">👫 ${{escapeHtml(INDIS[sid].clean_name)}}</a>`;
      }}
    }});
    html += `</div></div>`;
  }}

  // Notes
  if (p.notes && p.notes.length > 0) {{
    html += `<div class="detail-group"><h3>Архивные пометки и пояснения</h3>`;
    p.notes.forEach(n => {{
      html += `<div class="detail-item" style="background:var(--bg-primary); padding:0.55rem 0.75rem; border-radius:6px; border:1px solid var(--border-color); margin-bottom:0.35rem;">📝 ${{escapeHtml(n)}}</div>`;
    }});
    html += `</div>`;
  }}

  document.getElementById('modalBody').innerHTML = html;
  document.getElementById('personModal').classList.add('open');
}}

function closeModal() {{
  document.getElementById('personModal').classList.remove('open');
}}
function closeModalOnOverlay(e) {{
  if (e.target.id === 'personModal') closeModal();
}}

// TAB 2: GENERATIONS LIST
function renderGenerations() {{
  const container = document.getElementById('generationsContainer');
  container.innerHTML = '';

  const genMap = {{}};
  for (let i = 1; i <= 20; i++) genMap[i] = [];
  Object.values(INDIS).forEach(p => {{
    if (onlyDirectLine && !directAncestorIds.has(p.id)) return;
    const g = p.gen || 1;
    if (genMap[g]) genMap[g].push(p);
  }});

  for (let g = 1; g <= 20; g++) {{
    if (genMap[g].length === 0) continue;

    const section = document.createElement('div');
    section.className = 'gen-section';

    const count = genMap[g].length;
    const countLabel = onlyDirectLine ? (count === 1 ? '1 прямой предок' : `${{count}} прямых предка`) : (count === 1 ? '1 персона' : `${{count}} персон`);

    const title = document.createElement('div');
    title.className = 'gen-title';
    title.innerHTML = `<span>${{genTitles[g]}}</span> <span style="font-size:0.85rem; color:var(--text-muted); font-weight:normal;">${{countLabel}}</span> <button class="pill-btn" onclick="focusGeneration(${{g}});" style="font-size:0.75rem; margin-left:auto; display:inline-flex; align-items:center; gap:0.25rem;">🎯 На древо</button>`;
    section.appendChild(title);

    const grid = document.createElement('div');
    grid.className = 'cards-grid';

    genMap[g].sort((a,b) => a.clean_name.localeCompare(b.clean_name));
    genMap[g].forEach(p => {{
      const isReconstructed = !!p.is_reconstructed;
      const personDocs = getPersonDocs(p.id);
      const hasDocs = personDocs.length > 0;
      const card = document.createElement('div');
      card.className = `person-card sex-${{p.sex}} ${{p.id === 'I1' ? 'is-proband' : ''}} ${{hasDocs ? 'has-archival-docs' : ''}} ${{isReconstructed ? 'is-reconstructed' : ''}}`;
      card.style.position = 'relative';
      card.style.width = '100%';
      card.style.height = '85px';
      card.onclick = () => openModal(p.id);

      const sexIcon = p.sex === 'M' ? '♂' : '♀';
      const dates = p.display_birt ? `${{p.display_birt}}${{p.display_deat ? ' – ' + p.display_deat : ''}}` : (p.display_deat ? `ум. ${{p.display_deat}}` : '');
      const isVeteran = (p.id === 'I19' || p.id === 'I67' || p.id === 'I68' || p.id === 'I25' || p.id === 'I23' || p.id === 'I21' || p.id === 'I314' || p.id === 'I315' || p.id === 'I400' || p.id === 'I407' || p.id === 'I408' || p.id === 'I417' || p.id === 'I414' || p.id === 'I417');
      let vetBadge = '';
      if (p.id === 'I400' || p.id === 'I414' || p.id === 'I417') {{
        vetBadge = '<span class="badge-veteran" style="background:#fee2e2; color:#991b1b; border:1px solid #f87171;" title="Участник Отечественной войны 1812 года (рекрут / ратник-стрелок Вологодского ополчения)">🎖️ 1812 г.</span>';
      }} else if (p.id === 'I407' || p.id === 'I408' || p.id === 'I417') {{
        vetBadge = '<span class="badge-veteran" style="background:#ffedd5; color:#9a3412; border:1px solid #fb923c;" title="Участник Заграничного похода русской армии 1813 года (рекрут 1813 г.)">🎖️ 1813 г.</span>';
      }} else if (p.id === 'I25') {{
        vetBadge = '<span class="badge-veteran" title="Ветеран Первой мировой и Великой Отечественной войн">🎖️ ПМВ / ВОВ</span>';
      }} else if (p.id === 'I21') {{
        vetBadge = '<span class="badge-veteran" title="Младший лейтенант ВОВ, кавалер Ордена Отечественной войны I степени">🎖️ ВОВ</span>';
      }} else if (p.id === 'I314' || p.id === 'I315') {{
        vetBadge = '<span class="badge-veteran" title="Участник Великой Отечественной войны (погиб на фронте в 1942 г.)">🎖️ ВОВ</span>';
      }} else if (p.id === 'I68' || p.id === 'I23') {{
        vetBadge = '<span class="badge-veteran" title="Участник Великой Отечественной войны">🎖️ ВОВ</span>';
      }} else if (isVeteran) {{
        vetBadge = '<span class="badge-veteran" title="Герой Великой Отечественной войны">🎖️ ВОВ</span>';
      }}

      let reconBadge = '';
      if (isReconstructed) {{
        reconBadge = '<span class="badge-reconstructed" title="Научная реконструкция промежуточного поколения XVI века (акты утрачены)">⏳ XVI в.</span>';
      }}

      let docBadge = '';
      if (hasDocs) {{
        const firstDocIdx = DOCS.indexOf(personDocs[0]);
        docBadge = `<span class="badge-doc-tree" onclick="event.stopPropagation(); openDocViewer(${{firstDocIdx}}, getPersonDocs('${{p.id}}'));" title="Смотреть архивные документы (${{personDocs.length}})">🏛️ ${{personDocs.length}}</span>`;
      }}

      card.innerHTML = `
        <div class="card-top">
          <span class="card-gen">Пок. ${{p.gen}}</span>
          <div style="display:flex; align-items:center; gap:0.25rem;">
            ${{reconBadge}}
            ${{docBadge}}
            ${{vetBadge}}
            <span class="card-sex" style="color:${{p.sex === 'M' ? 'var(--male-border)' : 'var(--female-border)'}};">${{sexIcon}}</span>
          </div>
        </div>
        <div class="card-name">${{escapeHtml(p.clean_name)}}</div>
        <div class="card-meta">
          <span class="card-dates">${{dates || '—'}}</span>
          <span class="card-place">${{p.birt_plac ? '📍 ' + escapeHtml(p.birt_plac) : ''}}</span>
        </div>
        <div class="card-tag" style="background:${{p.branch_color}}18; color:${{p.branch_color}};">${{p.branch}}</div>
      `;
      grid.appendChild(card);
    }});

    section.appendChild(grid);
    container.appendChild(section);
  }}
}}

// TAB 3: TABLE
function renderTable() {{
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  const list = Object.values(INDIS).sort((a,b) => (a.gen - b.gen) || a.clean_name.localeCompare(b.clean_name));
  list.forEach((p, idx) => {{
    const tr = document.createElement('tr');
    tr.onclick = () => openModal(p.id);
    tr.innerHTML = `
      <td><strong>${{idx + 1}}</strong></td>
      <td><strong>${{escapeHtml(p.clean_name)}}</strong></td>
      <td>${{p.sex === 'M' ? 'Муж' : 'Жен'}}</td>
      <td>Пок. ${{p.gen}}</td>
      <td>${{p.display_birt || '—'}}</td>
      <td>${{p.display_deat || '—'}}</td>
      <td>${{p.birt_plac ? '📍 ' + escapeHtml(p.birt_plac) : '—'}}</td>
      <td><span style="color:${{p.branch_color}}; font-weight:600;">${{p.branch}}</span></td>
    `;
    tbody.appendChild(tr);
  }});
}}

// SEARCH
function handleSearch(q) {{
  q = q.trim().toLowerCase();
  clearHighlight();

  if (q.length >= 2) {{
    let firstFoundId = null;
    Object.values(INDIS).forEach(p => {{
      const match = p.clean_name.toLowerCase().includes(q) ||
                    (p.birt_plac && p.birt_plac.toLowerCase().includes(q)) ||
                    (p.notes && p.notes.some(n => n.toLowerCase().includes(q)));
      const card = document.getElementById(`card-${{p.id}}`);
      if (card) {{
        if (match) {{
          card.classList.add('highlighted');
          if (!firstFoundId) firstFoundId = p.id;
        }} else {{
          card.classList.remove('highlighted');
        }}
      }}
    }});
    if (firstFoundId && currentTab === 'tree') {{
      focusPerson(firstFoundId);
    }}
  }}

  document.querySelectorAll('#tableBody tr').forEach(tr => {{
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  }});
}}

function toggleTheme() {{
  const isDark = document.body.getAttribute('data-theme') === 'dark';
  document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
  updateDrawerThemeLabel();
}}

function escapeHtml(str) {{
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}}

document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{
    const fsScan = document.getElementById('fsScanModal');
    if (fsScan && fsScan.classList.contains('open')) {{
      closeFsScan();
      return;
    }}
    const viewer = document.getElementById('docViewerModal');
    if (viewer && viewer.classList.contains('open')) {{
      closeDocViewer();
      return;
    }}
    closeModal();
  }}
  const isFsOpen = document.getElementById('fsScanModal') && document.getElementById('fsScanModal').classList.contains('open');
  if (isFsOpen) {{
    if (e.key === '+' || e.key === '=') fsZoomIn();
    if (e.key === '-' || e.key === '_') fsZoomOut();
    if (e.key === '0') fsResetZoom();
    return;
  }}
  const isViewerOpen = document.getElementById('docViewerModal') && document.getElementById('docViewerModal').classList.contains('open');
  if (isViewerOpen) {{
    if (e.key === 'ArrowLeft') docPrev();
    if (e.key === 'ArrowRight') docNext();
  }}
}});

window.onload = init;
</script>
</body>
</html>
'''

with open('tree.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('родословная.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("tree.html, родословная.html and index.html regenerated successfully!")

