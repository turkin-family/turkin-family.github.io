"""
scripts/enrich_1834_and_fix_gens.py
Внесение недостающих связей по 8-й ревизии 1834 г. (Усть-Вымский приказ),
добавление пропущенных членов семей (жены, братья, племянники, старейшины),
исправление расчета поколений (gen) и пересчет координат раскладки.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, re
import data_manager

def run():
    persons = data_manager.load_persons()
    families = data_manager.load_families()
    sources = data_manager.load_sources()
    evidence = data_manager.load_evidence()

    p_dict = {p['id']: p for p in persons}
    f_dict = {f['id']: f for f in families}

    plac_uv = 'погост Усть-Вымский, Усть-Вымский приказ, Яренский уезд'
    plac_ser = 'деревня Серьяницкая, Усть-Вымский приказ, Яренский уезд'

    new_persons_def = [
        # Семья 8 (Фадей Туркин и дети)
        {
            'id': 'I198',
            'name': 'Фадей /Туркин/',
            'givn': 'Фадей',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1755',
            'birt_plac': plac_uv,
            'deat_date': 'до 1816',
            'deat_plac': plac_uv,
            'notes': ['Отец Алексея Фадеевича [I107] и Якова Фадеевича [I108] Туркиных. 8-я ревизия 1834 г. (л. 158 об., семья 8).']
        },
        {
            'id': 'I199',
            'name': 'Фадеевна /Туркина/',
            'givn': 'Фадеевна',
            'surn': 'Туркина',
            'sex': 'F',
            'birt_date': 'ок. 1785',
            'birt_plac': plac_uv,
            'notes': ['Сестра Алексея и Якова Фадеевых, мать Михаила Туркина [I110]. 8-я ревизия 1834 г. (л. 158 об., семья 8): «незаконнорожденный сын сестры его Михаило».']
        },
        # Семья 11 (пропущенные члены семьи)
        {
            'id': 'I200',
            'name': 'Иван /Туркин/',
            'givn': 'Иван',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1760',
            'birt_plac': plac_uv,
            'deat_date': 'до 1816',
            'deat_plac': plac_uv,
            'notes': ['Муж Офимьи Васильевны [I132], отец Ивана [I133], Петра [I203] и Емельяна [I206] Туркиных. 8-я ревизия 1834 г. (л. 159 об. - 160, семья 11).']
        },
        {
            'id': 'I201',
            'name': 'Василиса /Туркина/',
            'givn': 'Василиса',
            'surn': 'Туркина',
            'sex': 'F',
            'birt_date': 'ок. 1803',
            'birt_plac': plac_uv,
            'notes': ['Жена умершего Ивана Ивановича Туркина [I133], 31 год. 8-я ревизия 1834 г. (л. 160, семья 11).']
        },
        {
            'id': 'I202',
            'name': 'Парасковья Ивановна /Туркина/',
            'givn': 'Парасковья Ивановна',
            'surn': 'Туркина',
            'sex': 'F',
            'birt_date': 'ок. 1825',
            'birt_plac': plac_uv,
            'notes': ['Дочь Ивана Ивановича Туркина [I133] и Василисы [I201], 9 лет. 8-я ревизия 1834 г. (л. 160, семья 11).']
        },
        {
            'id': 'I203',
            'name': 'Пётр Иванович /Туркин/',
            'givn': 'Пётр Иванович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1799',
            'birt_plac': plac_uv,
            'notes': ['Брат Ивана Иванова, сын Офимьи Васильевны, 17 лет в 1816 г., 35 лет в 1834 г. 8-я ревизия 1834 г. (л. 159 об., семья 11).']
        },
        {
            'id': 'I204',
            'name': 'Ирина /Туркина/',
            'givn': 'Ирина',
            'surn': 'Туркина',
            'sex': 'F',
            'birt_date': 'ок. 1812',
            'birt_plac': plac_uv,
            'notes': ['Жена Петра Ивановича Туркина [I203], 22 года. 8-я ревизия 1834 г. (л. 160, семья 11).']
        },
        {
            'id': 'I205',
            'name': 'Андрей Петрович /Туркин/',
            'givn': 'Андрей Петрович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': '1833',
            'birt_plac': plac_uv,
            'notes': ['Сын Петра Ивановича [I203] и Ирины [I204], новорожденный 13 месяцев. 8-я ревизия 1834 г. (л. 159 об., семья 11).']
        },
        {
            'id': 'I206',
            'name': 'Емельян Иванович /Туркин/',
            'givn': 'Емельян Иванович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1803',
            'birt_plac': plac_uv,
            'notes': ['2-й брат Ивана Иванова, сын Офимьи Васильевны, 13 лет в 1816 г., 31 год в 1834 г. 8-я ревизия 1834 г. (л. 159 об., семья 11).']
        },
        {
            'id': 'I207',
            'name': 'Ульяна /Туркина/',
            'givn': 'Ульяна',
            'surn': 'Туркина',
            'sex': 'F',
            'birt_date': 'ок. 1811',
            'birt_plac': plac_uv,
            'notes': ['Жена Емельяна Ивановича Туркина [I206], 23 года. 8-я ревизия 1834 г. (л. 160, семья 11).']
        },
        # Семья 25 (Василий Туркин)
        {
            'id': 'I208',
            'name': 'Василий /Туркин/',
            'givn': 'Василий',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1755',
            'birt_plac': plac_uv,
            'deat_date': 'до 1816',
            'deat_plac': plac_uv,
            'notes': ['Отец Ивана Васильевича [I136] и Герасима Васильевича [I142] Туркиных. 8-я ревизия 1834 г. (л. 162 об., семья 25).']
        },
        # Семья 71 и 72 (Алексей Туркин и незаконнорожденные племянники Степан и Яков)
        {
            'id': 'I209',
            'name': 'Алексей /Туркин/',
            'givn': 'Алексей',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1728',
            'birt_plac': plac_uv,
            'deat_date': 'до 1816',
            'deat_plac': plac_uv,
            'notes': ['Отец старейшины Афанасия Алексеевича [I162], Ивана Алексеевича [I169], Матрёны [I175], Пелагеи [I176] и Катерины [I177] Туркиных. 8-я ревизия 1834 г. (лл. 174 об. - 175, семьи 71 и 72).']
        },
        {
            'id': 'I210',
            'name': 'Степан /Туркин/',
            'givn': 'Степан',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1818',
            'birt_plac': plac_uv,
            'notes': ['Незаконнорожденный сын 1-й сестры Матрёны Алексеевны [I175], племянник Ивана Алексеева, 16 лет в 1834 г. 8-я ревизия 1834 г. (л. 174 об., семья 72).']
        },
        {
            'id': 'I211',
            'name': 'Яков /Туркин/',
            'givn': 'Яков',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1821',
            'birt_plac': plac_uv,
            'notes': ['Незаконнорожденный сын 2-й сестры Пелагеи Алексеевны [I176], племянник Ивана Алексеева, 13 лет в 1834 г. 8-я ревизия 1834 г. (л. 174 об., семья 72).']
        },
        # Семья 86 (деревня Серьяницкая - Пётр и Прохор)
        {
            'id': 'I212',
            'name': 'Пётр /Туркин/',
            'givn': 'Пётр',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1725',
            'birt_plac': plac_ser,
            'deat_date': 'до 1816',
            'deat_plac': plac_ser,
            'notes': ['Отец Николая Петровича [I194] и Прохора Петровича [I213] Туркиных. 8-я ревизия 1834 г. (л. 177 об., семья 86, деревня Серьяницкая).']
        },
        {
            'id': 'I213',
            'name': 'Прохор Петрович /Туркин/',
            'givn': 'Прохор Петрович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1765',
            'birt_plac': plac_ser,
            'deat_date': 'до 1816',
            'deat_plac': plac_ser,
            'notes': ['Брат Николая Петровича [I194], отец Фёдора Прохоровича [I197]. 8-я ревизия 1834 г. (л. 177 об., семья 86).']
        },
        # Семья 83 (л. 177 об.)
        {
            'id': 'I214',
            'name': 'Григорий Егорович /Туркин/',
            'givn': 'Григорий Егорович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1776',
            'birt_plac': plac_uv,
            'notes': ['40 лет в 1816 г., 58 лет в 1834 г. 8-я ревизия 1834 г. (л. 177 об., семья 83).']
        },
        {
            'id': 'I215',
            'name': 'Григорий Григорьевич /Туркин/',
            'givn': 'Григорий Григорьевич',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1802',
            'birt_plac': plac_uv,
            'deat_date': '1829',
            'deat_plac': plac_uv,
            'notes': ['Сын Григория Егорова [I214], 14 лет в 1816 г., умре в 1829 году. 8-я ревизия 1834 г. (л. 177 об., семья 83).']
        },
        # Семья 55 (л. 170 об.)
        {
            'id': 'I216',
            'name': 'Илья Петрович /Туркин/',
            'givn': 'Илья Петрович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1763',
            'birt_plac': plac_uv,
            'notes': ['53 года в 1816 г., 71 год в 1834 г. 8-я ревизия 1834 г. (л. 170 об., семья 55).']
        },
        {
            'id': 'I217',
            'name': 'Михайло Ильич /Туркин/',
            'givn': 'Михайло Ильич',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1806',
            'birt_plac': plac_uv,
            'notes': ['Сын Ильи Петрова [I216], 10 лет в 1816 г., 28 лет в 1834 г. 8-я ревизия 1834 г. (л. 170 об., семья 55).']
        },
        {
            'id': 'I218',
            'name': 'Иван Михайлович /Туркин/',
            'givn': 'Иван Михайлович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': '1831',
            'birt_plac': plac_uv,
            'notes': ['Сын Михайла Ильина [I217], 3 года 2 месяца. 8-я ревизия 1834 г. (л. 170 об., семья 55).']
        },
        {
            'id': 'I219',
            'name': 'Василий Михайлович /Туркин/',
            'givn': 'Василий Михайлович',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': '1834',
            'birt_plac': plac_uv,
            'notes': ['Сын Михайла Ильина [I217], 1 месяц. 8-я ревизия 1834 г. (л. 170 об., семья 55).']
        },
        {
            'id': 'I220',
            'name': 'Яков Ильич /Туркин/',
            'givn': 'Яков Ильич',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1809',
            'birt_plac': plac_uv,
            'notes': ['2-й сын Ильи Петрова [I216], 7 лет в 1816 г., 25 лет в 1834 г. 8-я ревизия 1834 г. (л. 170 об., семья 55).']
        },
        # Семья 87 (л. 177 об.)
        {
            'id': 'I221',
            'name': 'Пётр Васильевич /Туркин/',
            'givn': 'Пётр Васильевич',
            'surn': 'Туркин',
            'sex': 'M',
            'birt_date': 'ок. 1784',
            'birt_plac': plac_uv,
            'notes': ['32 года в 1816 г., зять Василия Ивановича (Сизова/Клюкова). 8-я ревизия 1834 г. (л. 177 об., семья 87).']
        }
    ]

    # Добавляем новых персон
    for np in new_persons_def:
        if np['id'] not in p_dict:
            persons.append(np)
            p_dict[np['id']] = np

    # Обновляем или добавляем семьи
    families_updates = [
        # Семья 8
        {'id': 'F74', 'husb': 'I198', 'wife': None, 'children': ['I107', 'I108', 'I199']},
        {'id': 'F75', 'husb': None, 'wife': 'I199', 'children': ['I110']},
        # Семья 11: F57 и F58 обновляем
        {'id': 'F57', 'husb': 'I200', 'wife': 'I132', 'children': ['I133', 'I203', 'I206']},
        {'id': 'F58', 'husb': 'I133', 'wife': 'I201', 'children': ['I134', 'I202']},
        {'id': 'F76', 'husb': 'I203', 'wife': 'I204', 'children': ['I205']},
        {'id': 'F77', 'husb': 'I206', 'wife': 'I207', 'children': []},
        # Семья 25
        {'id': 'F78', 'husb': 'I208', 'wife': None, 'children': ['I136', 'I142']},
        # Семьи 71 и 72
        {'id': 'F79', 'husb': 'I209', 'wife': None, 'children': ['I162', 'I169', 'I175', 'I176', 'I177']},
        {'id': 'F80', 'husb': None, 'wife': 'I175', 'children': ['I210']},
        {'id': 'F81', 'husb': None, 'wife': 'I176', 'children': ['I211']},
        # Семья 86 (д. Серьяницкая)
        {'id': 'F82', 'husb': 'I212', 'wife': None, 'children': ['I194', 'I213']},
        {'id': 'F83', 'husb': 'I213', 'wife': None, 'children': ['I197']},
        # Семья 83
        {'id': 'F84', 'husb': 'I214', 'wife': None, 'children': ['I215']},
        # Семья 55
        {'id': 'F85', 'husb': 'I216', 'wife': None, 'children': ['I217', 'I220']},
        {'id': 'F86', 'husb': 'I217', 'wife': None, 'children': ['I218', 'I219']}
    ]

    for fu in families_updates:
        fid = fu['id']
        existing = next((f for f in families if f['id'] == fid), None)
        if existing:
            existing['husb'] = fu['husb']
            existing['wife'] = fu['wife']
            existing['children'] = fu['children']
        else:
            families.append(fu)

    # Обновляем документ-источник
    s_doc = next((d for d in sources['documents'] if d['id'] == 'revision_1834_ustvym_economic'), None)
    if s_doc:
        s_doc['personIds'] = [f'I{i}' for i in range(107, 222)]

    # Добавляем evidence records
    ev_person_ids = {e.get('person_id') for e in evidence}
    ev_max_id = max(int(e['evidence_id'].replace('EVD_', '')) for e in evidence if 'evidence_id' in e)
    for pid_int in range(198, 222):
        pid = f'I{pid_int}'
        if pid not in ev_person_ids:
            ev_max_id += 1
            pname = p_dict[pid]['name']
            evidence.append({
                'evidence_id': f'EVD_{ev_max_id:04d}',
                'person_id': pid,
                'person_name': pname,
                'source_id': 'revision_1834_ustvym_economic',
                'source_title': '8-я ревизия 1834 г.: экономические крестьяне Усть-Вымского приказа (Туркины)',
                'archive_reference': 'ГАВО, ф. 388, оп. 10, д. 70, лл. 158 об. – 177 об.',
                'date': '1834 год',
                'citation_summary': f'Запись в 8-й ревизии 1834 г. экономических крестьян Усть-Вымского волостного приказа (ГАВО, ф. 388, оп. 10, д. 70, лл. 158 об. – 177 об.) для персоны {pname}.',
                'badge': '8-я ревизия 1834 г. (Усть-Вымь)'
            })

    # ==========================================================
    # ТОЧНЫЙ РАСЧЕТ ПОКОЛЕНИЙ ДЛЯ ВСЕХ ПЕРСОН (1..15)
    # ==========================================================
    def parse_year(s):
        if not s:
            return None
        m = re.search(r'\b(1[6789]\d{2}|20\d{2})\b', s)
        return int(m.group(1)) if m else None

    # Фиксированные сиды поколений
    ancient_seeds = {
        'I1': 1,
        'I70': 8,
        'I77': 9,
        'I75': 10,
        'I71': 11,
        'I72': 12,
        'I73': 13,
        'I74': 14,
        'I88': 12,
    }

    gens = dict(ancient_seeds)

    # 1. Распространяем от сидов по существующим связям
    changed = True
    while changed:
        changed = False
        for f in families:
            h, w = f.get('husb'), f.get('wife')
            ch = f.get('children', [])
            for c in ch:
                if c in gens:
                    cg = gens[c]
                    if h and (h not in gens or gens[h] < cg + 1):
                        gens[h] = cg + 1
                        changed = True
                    if w and (w not in gens or gens[w] < cg + 1):
                        gens[w] = cg + 1
                        changed = True
            pg = [gens[p] for p in [h, w] if p and p in gens]
            if pg:
                c_target = min(pg) - 1
                for c in ch:
                    if c == 'I70': continue
                    if c not in gens or gens[c] != c_target:
                        gens[c] = c_target
                        changed = True
            if h and w:
                if h in gens and w not in gens:
                    gens[w] = gens[h]
                    changed = True
                elif w in gens and h not in gens:
                    gens[h] = gens[w]
                    changed = True

    # 2. Для всех остальных вычисляем поколение по году рождения:
    # 1995 -> 1
    # 1965 -> 2
    # 1935 -> 3
    # 1905 -> 4
    # 1875 -> 5
    # 1845 -> 6
    # 1815 -> 7
    # 1785 -> 8
    # 1755 -> 9
    # 1725 -> 10
    # 1695 -> 11
    # 1665 -> 12
    for p in persons:
        pid = p['id']
        if pid not in gens:
            yr = parse_year(p.get('birt_date'))
            if not yr:
                yr = parse_year(p.get('deat_date'))
                if yr: yr -= 50
            if yr:
                g = max(1, min(15, round((1995 - yr) / 30) + 1))
                gens[pid] = g
            else:
                gens[pid] = 7

    # 3. Итеративное согласование внутри семейных компонент
    changed = True
    iterations = 0
    while changed and iterations < 50:
        changed = False
        iterations += 1
        for f in families:
            h, w = f.get('husb'), f.get('wife')
            ch = f.get('children', [])
            # Родители должны быть строго больше детей (child_gen + 1)
            c_gens = [gens[c] for c in ch if c in gens]
            if c_gens:
                expected_p = max(c_gens) + 1
                if h and gens[h] < expected_p:
                    gens[h] = expected_p
                    changed = True
                if w and gens[w] < expected_p:
                    gens[w] = expected_p
                    changed = True

            # Дети должны быть не выше родителей
            p_gens = [gens[p] for p in [h, w] if p and p in gens]
            if p_gens:
                max_allowed_c = min(p_gens) - 1
                for c in ch:
                    if c == 'I70': continue
                    if gens[c] > max_allowed_c:
                        gens[c] = max_allowed_c
                        changed = True

            # Супруги на одном уровне
            if h and w and h in gens and w in gens:
                if gens[h] != gens[w]:
                    mg = max(gens[h], gens[w])
                    gens[h] = mg
                    gens[w] = mg
                    changed = True

            # Сиблинги на одном уровне
            if ch:
                s_gens = [gens[c] for c in ch if c in gens and c != 'I70']
                if s_gens:
                    max_s = max(s_gens)
                    for c in ch:
                        if c == 'I70': continue
                        if gens[c] < max_s:
                            gens[c] = max_s
                            changed = True

    # Записываем gen в каждого человека
    for p in persons:
        p['gen'] = gens.get(p['id'], 7)

    # Сохраняем обновленные данные
    data_manager.save_persons(persons)
    data_manager.save_families(families)
    data_manager.save_sources(sources)
    data_manager.save_evidence(evidence)

    print(f"Persons count: {len(persons)}")
    print(f"Families count: {len(families)}")
    print(f"Evidence count: {len(evidence)}")
    print("Gen distribution for new persons I107..I221:")
    gen_dist = {}
    for p in persons:
        if int(p['id'].replace('I','')) >= 107:
            gen_dist[p['gen']] = gen_dist.get(p['gen'], 0) + 1
    for g in sorted(gen_dist.keys()):
        print(f"  Gen {g}: {gen_dist[g]} persons")

if __name__ == '__main__':
    run()
