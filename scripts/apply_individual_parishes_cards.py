#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_individual_parishes_cards.py

Creates individual document cards and evidence links for each of the
14 specific biographies on parishes.ru (http://parishes.ru/pers.php?no=57),
using the dedicated cropped screenshots and thumbnails.
"""

import json

def run():
    with open('data/sources.json') as f: sources = json.load(f)
    with open('data/evidence.json') as f: evidence = json.load(f)
    with open('data/persons.json') as f: persons = json.load(f)

    # 1. Map of individual entries from parishes.ru
    parishes_entries = [
        {
            "id": "parishes_14118",
            "title": "parishes.ru: о. Автоном Лаврентьевич Туркин (священник с. Оквад)",
            "personId": "I245",
            "personIds": ["I245", "I246"],
            "personName": "Священник Автоном Лаврентьевич Туркин и дочь Марина",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14118",
            "badgeColor": "#0284c7",
            "date": "1731–1736 гг.",
            "archive": "parishes.ru (№ 14118) / ВУЦА ф. 363, ГААО ф. 29",
            "award": "Введенская церковь погоста Оквад",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14118.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14118.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14118",
            "desc": "В 1731, 1736 гг. — священник Введенской церкви Оквадской волости Яренского уезда Великоустюжской епархии. Дочь Марина, жена Пешкилева Федора Иванова. Источники: ВУЦА. Ф. 363. Оп. 1. Д. 59. Л. 11 (Разбор 1736 г.); ГААО. Ф. 29. Оп. 27. Д. 1. Л. 44 (МК 1731 г.); Д. 2. Л. 79 (МК 1734 г.)."
        },
        {
            "id": "parishes_1035",
            "title": "parishes.ru: о. Алексей Елисеевич Туркин (диакон с. Коквицы)",
            "personId": "I234",
            "personIds": ["I234"],
            "personName": "Диакон Алексей Елисеевич Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #1035",
            "badgeColor": "#0284c7",
            "date": "1830 г.",
            "archive": "parishes.ru (№ 1035) / НА РК ф. 254 (Клировые ведомости)",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_1035.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_1035.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#1035",
            "desc": "В 1830 г. — диакон Христорождественской церкви с. Коквицы Яренского уезда. Сын пономаря Елисея Леонтьевича Туркина. Источник: НА РК. Ф. 254. Оп. 1. Д. 26. Л. 11 об."
        },
        {
            "id": "parishes_13958",
            "title": "parishes.ru: о. Алексей Тимофеевич Туркин (священник с. Палевицы)",
            "personId": "I239",
            "personIds": ["I239", "I240", "I243", "I244"],
            "personName": "Священник Алексей Тимофеевич Туркин и семья",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #13958",
            "badgeColor": "#0284c7",
            "date": "1734–1755 гг.",
            "archive": "parishes.ru (№ 13958) / ВУЦА ф. 363, ГААО ф. 29",
            "award": "Покровская церковь с. Палевицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_13958.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_13958.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#13958",
            "desc": "В 1734–1755 гг. — священник Покровской церкви Палевицкой волости. Супруга Матрона. Дети: Михаил (соборный сторож Яренска), Андрей, Марфа (жена пономаря с. Часово Афанасия Попова). Источники: ВУЦА. Ф. 363. Оп. 1. Д. 59. Л. 10; ГААО. Ф. 29. Оп. 27. Д. 2. Л. 71; Д. 3. Л. 179."
        },
        {
            "id": "parishes_1116",
            "title": "parishes.ru: Елисей Леонтьевич Туркин (пономарь с. Коквицы)",
            "personId": "I232",
            "personIds": ["I232", "I233"],
            "personName": "Пономарь Елисей Леонтьевич Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #1116",
            "badgeColor": "#0284c7",
            "date": "1795–1834 гг.",
            "archive": "parishes.ru (№ 1116) / ГАВО ф. 388, НА РК",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_1116.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_1116.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#1116",
            "desc": "Пономарь Христорождественской церкви с. Коквицы. Сын пономаря Леонтия Петровича Туркина. Жена Татьяна Васильевна Пономарёва. Дети: Иоанн и Алексей (диакон). Источники: ГАВО. Ф. 388. Оп. 1. Д. 8467. Л. 7 (РС 1795); Д. 9496. Л. 15 (РС 1834); НА РК. Клировые ведомости."
        },
        {
            "id": "parishes_1126",
            "title": "parishes.ru: Иван Елисеевич Туркин (с. Коквицы)",
            "personId": "I238",
            "personIds": ["I238"],
            "personName": "Иван Елисеевич Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #1126",
            "badgeColor": "#0284c7",
            "date": "XIX в.",
            "archive": "parishes.ru (№ 1126) / НА РК ф. 254",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_1126.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_1126.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#1126",
            "desc": "Сын пономаря Елисея Леонтьевича Туркина и Татьяны Васильевны (Пономарёвой), брат диакона Алексея Елисеевича Туркина. Источник: НА РК. Клировые ведомости с. Коквицы."
        },
        {
            "id": "parishes_14654",
            "title": "parishes.ru: о. Иван Петрович Туркин (священник с. Коквицы)",
            "personId": "I71",
            "personIds": ["I71"],
            "personName": "Священник Иван Петрович Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14654",
            "badgeColor": "#0284c7",
            "date": "1710–1747 гг.",
            "archive": "parishes.ru (№ 14654, 14254) / РГАДА д. 1081, ГААО ф. 29",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14654.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14654.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14654",
            "desc": "В переписи 1710 г. — 22 года, при Коквицкой церкви; жена Татьяна 19 лет, сын Стефан 1 год. В 1747 г. — священник Христорождественской церкви с. Коквицы. Источники: РГАДА. Ф. 1209. Оп. 1. Д. 1081. Л. 236; ГААО. Ф. 29. Оп. 27. Д. 3. Л. 94 об."
        },
        {
            "id": "parishes_14873",
            "title": "parishes.ru: Исаакий Афанасьевич Туркин (дьячок с. Оквад)",
            "personId": "I73",
            "personIds": ["I73", "I74", "I92", "I95"],
            "personName": "Дьячок Исаакий Афанасьевич Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14873",
            "badgeColor": "#0284c7",
            "date": "1678 г.",
            "archive": "parishes.ru (№ 14873) / РГАДА ф. 1209, д. 1081",
            "award": "Введенская церковь погоста Оквад",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14873.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14873.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14873",
            "desc": "В 1678 г. — дьячок Введенской церкви Оквадской волости. Сын Афанасия Семёновича Туркина (жителя погоста Катвад / Оквад). Дети: Пётр, Тимофей, Ларион. Источник: РГАДА. Ф. 1209. Оп. 1. Д. 1081."
        },
        {
            "id": "parishes_13343",
            "title": "parishes.ru: Леонтий Петрович Туркин (пономарь с. Коквицы)",
            "personId": "I230",
            "personIds": ["I230", "I231"],
            "personName": "Пономарь Леонтий Петрович Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #13343",
            "badgeColor": "#0284c7",
            "date": "1745–1755 гг.",
            "archive": "parishes.ru (№ 13343) / РГИА ф. 796, ВУЦА ф. 363",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_13343.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_13343.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#13343",
            "desc": "Пономарь Христорождественской церкви с. Коквицы (посвящен в 1745 г.). Сын пономаря Петра Петровича Туркина. Жена Агриппина Ивановна Васева, сын Елисей. Источники: РГИА. Ф. 796. Оп. 36. Д. 344; ВУЦА. Ф. 363. Оп. 1. Д. 85. Л. 7."
        },
        {
            "id": "parishes_13959",
            "title": "parishes.ru: Михаил Алексеевич Туркин (сторож собора г. Яренска)",
            "personId": "I241",
            "personIds": ["I241", "I242"],
            "personName": "Михаил Алексеевич Туркин (Яренск)",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #13959",
            "badgeColor": "#0284c7",
            "date": "1745–1747 гг.",
            "archive": "parishes.ru (№ 13959) / ВУЦА ф. 363, ГААО ф. 29",
            "award": "Богоявленский собор г. Яренска",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_13959.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_13959.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#13959",
            "desc": "В 1745 г. — соборный сторож г. Яренска. Сын священника с. Палевицы Алексея Тимофеевича Туркина. Жена Марфа Козьминична Ипатова. Источники: ВУЦА. Ф. 363. Оп. 1. Д. 85. Л. 12 об.; ГААО. Ф. 29. Оп. 27. Д. 3. Л. 218."
        },
        {
            "id": "parishes_2393",
            "title": "parishes.ru: о. Михаил Алексеевич Туркин (соборный диакон г. Лальска)",
            "personId": "I236",
            "personIds": ["I236", "I237"],
            "personName": "Диакон Михаил Алексеевич Туркин (Лальск)",
            "category": "ancient",
            "categoryLabel": "Духовенство Вологодской епархии",
            "badge": "parishes.ru #2393",
            "badgeColor": "#0284c7",
            "date": "1839–1904 гг.",
            "archive": "parishes.ru (№ 2393) / ГАКО ф. 1310, ВЕВ 1904",
            "award": "Воскресенский собор г. Лальска",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_2393.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_2393.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#2393",
            "desc": "1839 – 13.06.1904. Диакон Воскресенского собора города Лальска. Сын диакона Алексея Елисеевича Туркина. Супруга София Прокопьевна Брызгалова. Источники: ГАКО. Ф. 1310. Оп. 1. Д. 25. Лл. 68 об.–69 об.; ВЕВ. 1904. № 14. С. 269."
        },
        {
            "id": "parishes_14115",
            "title": "parishes.ru: о. Пётр Исаакович Туркин (священник с. Коквицы и Усть-Выми)",
            "personId": "I72",
            "personIds": ["I72", "I222", "I223", "I225", "I226"],
            "personName": "Священник Пётр Исаакович Туркин и супруга Епистимия",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14115",
            "badgeColor": "#0284c7",
            "date": "1696–1731 гг.",
            "archive": "parishes.ru (№ 14115) / ГААО ф. 29, РГАДА д. 1081",
            "award": "Коквицы и Благовещенская церковь Усть-Выми",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14115.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14115.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14115",
            "desc": "В 1696/97 и 1710 гг. — священник Христорождественской церкви в Коквицах. В 1731 г. — священник Благовещенской церкви Усть-Вымской волости. Жена Епистимия (ок. 1657 г.р.). Дети: Иван, Григорий, Пётр, Дарья, Епистимия. Источники: ГААО. Ф. 29. Оп. 27. Д. 1. Л. 40; РГАДА. Ф. 1209. Оп. 1. Д. 1081."
        },
        {
            "id": "parishes_14199",
            "title": "parishes.ru: Пётр Петрович Туркин (пономарь с. Коквицы)",
            "personId": "I224",
            "personIds": ["I224"],
            "personName": "Пономарь Пётр Петрович Туркин",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14199",
            "badgeColor": "#0284c7",
            "date": "1745–1755 гг.",
            "archive": "parishes.ru (№ 14199) / РГИА ф. 796, ВУЦА ф. 363",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14199.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14199.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14199",
            "desc": "Пономарь Христорождественской церкви с. Коквицы. Сын священника Петра Исааковича Туркина, отец пономаря Леонтия Петровича. Источники: РГИА. Ф. 796. Оп. 36. Д. 344; ВУЦА. Ф. 363. Оп. 1. Д. 85. Л. 7."
        },
        {
            "id": "parishes_1043",
            "title": "parishes.ru: Симеон Алексеевич Туркин (дьячок с. Ляли)",
            "personId": "I235",
            "personIds": ["I235"],
            "personName": "Дьячок Симеон Алексеевич Туркин (с. Ляли)",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #1043",
            "badgeColor": "#0284c7",
            "date": "XIX в.",
            "archive": "parishes.ru (№ 1043) / НА РК ф. 254",
            "award": "Богоявленская церковь с. Ляли",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_1043.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_1043.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#1043",
            "desc": "Дьячок Богоявленской церкви с. Ляли Яренского уезда. Сын диакона Алексея Елисеевича Туркина, брат диакона Михаила Алексеевича Туркина. Источник: НА РК. Клировые ведомости."
        },
        {
            "id": "parishes_14198",
            "title": "parishes.ru: о. Степан Иванович Туркин (священник с. Коквицы)",
            "personId": "I78",
            "personIds": ["I78", "I80", "I75", "I229"],
            "personName": "Священник Степан Иванович Туркин и сыновья",
            "category": "ancient",
            "categoryLabel": "Духовенство Яренского уезда",
            "badge": "parishes.ru #14198",
            "badgeColor": "#0284c7",
            "date": "1734–1773 гг.",
            "archive": "parishes.ru (№ 14198) / ГААО ф. 29, ВУЦА ф. 363, ВЦА ф. 363",
            "award": "Христорождественская церковь с. Коквицы",
            "file": "архив_сканы_первоисточников/parishes_entries/parishes_14198.png",
            "thumb": "архив_сканы_первоисточников/превью/thumb_parishes_14198.jpg",
            "web_source": "http://parishes.ru/pers.php?no=57#14198",
            "desc": "В 1734 и 1736 гг. — священник Христорождественской церкви с. Коквицы. Сын священника Ивана Петровича Туркина. Сыновья: Григорий (прямой предок), Иван, Пётр. В 1773 г. записан 62-летним вдовым попом (ВЦА, двор 167). Источники: ГААО. Ф. 29. Оп. 27. Д. 2. Л. 66; ВУЦА. Ф. 363. Оп. 1. Д. 59. Л. 12."
        }
    ]

    # Add to sources.json
    docs = sources.get('documents', [])
    existing_entry_ids = {d.get('id') for d in parishes_entries}
    docs = [d for d in docs if d.get('id') not in existing_entry_ids]
    docs.extend(parishes_entries)
    sources['documents'] = docs

    # Add evidence entries
    for entry in parishes_entries:
        doc_id = entry['id']
        for pid in entry['personIds']:
            # check if evidence already exists
            ev_exists = any(e.get('person_id') == pid and e.get('source_id') == doc_id for e in evidence)
            if not ev_exists:
                evidence.append({
                    "person_id": pid,
                    "source_id": doc_id,
                    "quote": entry['desc'][:140] + "...",
                    "page": entry['web_source'],
                    "year": entry.get('date', 'XVII-XIX вв.'),
                    "confidence": "высокая"
                })

    # Update persons notes with exact anchors
    person_to_anchor = {}
    for entry in parishes_entries:
        anchor = entry['web_source']
        for pid in entry['personIds']:
            person_to_anchor[pid] = anchor

    for p in persons:
        pid = p['id']
        if pid in person_to_anchor:
            anchor = person_to_anchor[pid]
            notes = p.get('notes', [])
            updated_notes = []
            for n in notes:
                if 'parishes.ru' in str(n):
                    updated_notes.append(f"Первоисточник биографии: База данных «Православные приходы и монастыри Севера» (parishes.ru), Персоналии № 57: Туркины ({anchor}).")
                else:
                    updated_notes.append(n)
            p['notes'] = updated_notes

    with open('data/sources.json', 'w', encoding='utf-8') as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)
    with open('data/evidence.json', 'w', encoding='utf-8') as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)
    with open('data/persons.json', 'w', encoding='utf-8') as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)

    print(f"Successfully added {len(parishes_entries)} individual parishes cards!")

if __name__ == '__main__':
    run()
