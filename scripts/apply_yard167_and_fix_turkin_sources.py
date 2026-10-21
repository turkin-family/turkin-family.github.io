#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_yard167_and_fix_turkin_sources.py
1. Объединение документов Коквицы в один чистый разворот 'revision_1816_turkin_kokvitsy' (лл. 352 об. – 353, семьи 157, 158, 159).
   Удаление дублирующих/фрагментированных документов 'revision_1816_family_158_159_male', 'revision_1816_family_158_159_female', 'revision_1816_family_157_turkin'.
   Проставление source_id = 'revision_1816_turkin_kokvitsy' всем коквицким Туркиным.
2. Двор № 166: связывание братьев Дениса (I430) и Михайла (I414) Кызъюровых в единую семью (F152) с отцом Фёдором (I431).
3. Двор № 167: внесение семьи Осипа Афанасьевича Изъюрова (I432), сына Фёдора (I433), жены Марьи (I434), сестры Федосьи (I435), детей Ивана (I436) и Анны (I437).
   Создание союзов F153 и F154.
4. Обновление архивного документа по Ибской (лл. 446 об. – 447, дворы 166 и 167).
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PERSONS_FILE = os.path.join(DATA_DIR, "persons.json")
FAMILIES_FILE = os.path.join(DATA_DIR, "families.json")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
COORDS_FILE = os.path.join(DATA_DIR, "calibrated_coords.json")
CATALOG_FILE = os.path.join(os.path.dirname(__file__), "..", "archive_catalog.py")

def main():
    with open(PERSONS_FILE, "r", encoding="utf-8") as f:
        persons = json.load(f)
    with open(FAMILIES_FILE, "r", encoding="utf-8") as f:
        families = json.load(f)
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_data = json.load(f)
    with open(COORDS_FILE, "r", encoding="utf-8") as f:
        coords = json.load(f)

    persons_by_id = {p["id"]: p for p in persons}
    families_by_id = {f["id"]: f for f in families}

    # -------------------------------------------------------------
    # 1. ОБЪЕДИНЕНИЕ ДОКУМЕНТОВ КОКВИЦЫ (убираем дублирование "лист 353 на всех")
    # -------------------------------------------------------------
    kokvitsy_pids = [
        "I148", "I80", "I81", "I79", "I368", "I369", "I370", "I371", "I372", "I373", "I374", "I375", "I376", "I377", "I378",
        "I379", "I380", "I381", "I382", "I383", "I384", "I385", "I386", "I387", "I388", "I389", "I390"
    ]
    # Назначаем source_id всем коквицким Туркиным
    for pid in kokvitsy_pids:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_turkin_kokvitsy"

    unified_kokvitsy_doc = {
        "id": "revision_1816_turkin_kokvitsy",
        "title": "7-я ревизия 1816 г.: Разворот Коквицкого селения (семьи Туркиных № 157, 158, 159, лл. 352 об. – 353)",
        "personId": "I148",
        "personIds": [pid for pid in kokvitsy_pids if pid in persons_by_id],
        "personName": "Алексей Григорьевич, Григорий Степанович и Иван Леонтьевич Туркины",
        "category": "ancient",
        "categoryLabel": "Ревизии и переписи",
        "badge": "7-я ревизия (Коквицы, лл. 352 об. – 353)",
        "badgeColor": "#2563eb",
        "date": "1816 год",
        "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 352 об. – 353 (семьи 157, 158, 159)",
        "award": "7-я Государственная подушная ревизия",
        "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_spread_352ob_353.jpg",
        "thumb": "превью/kokvitsy_thumb_352ob_353.jpg",
        "desc": (
            "Подлинный двухстраничный разворот 7-й ревизии 1816 года по Коквицкому селению (ГАВО, ф. 388, оп. 9, д. 201, лл. 352 об. – 353):\n"
            "• Двор № 157: глава двора Иван Леонтьев Туркин (44 года), сын Иван (7 лет), брат Михайло Леонтьев (29 лет); женский пол (л. 353): жена Ивана Устинья (27 лет), сестра Акилина (47 лет), дочери Марья (13 лет) и Анна (3 года).\n"
            "• Двор № 158: 6-й прадед Григорий Степанов Туркин (умре в 1814 г.), его сыновья Василий (33 года, сын Григорий 1 год), Григорий (28 лет), Иван старший (25 лет), Иван меньшой (21 год); женский пол (л. 353): жена Григория Степанова Матрёна (63 года, 6-я прабабушка), жена Василия Авдотья (25 лет, дочери Катерина 8 лет, Дарья 5 лет), жена Григория Анна (22 года), свояченица Пелагия (70 лет, род. ок. 1746 г.).\n"
            "• Двор № 159: прямой 5-й прадед Алексей Григорьев Туркин (38 лет), сыновья Иван старший (8 лет) и Иван 2-й (2 года); женский пол (л. 353): жена Алексея Афанасия (38 лет, 5-я прабабушка), дочери Наталья (12 лет) и Ирина (6 лет)."
        )
    }

    # Удаляем старые фрагментированные карточки и добавляем объединенный документ
    docs = sources_data.get("documents", [])
    obsolete_ids = {"revision_1816_family_158_159_male", "revision_1816_family_158_159_female", "revision_1816_family_157_turkin"}
    docs = [d for d in docs if d["id"] not in obsolete_ids and d["id"] != "revision_1816_turkin_kokvitsy"]
    docs.append(unified_kokvitsy_doc)

    # -------------------------------------------------------------
    # 2. ДВОР № 166: СВЯЗЫВАНИЕ БРАТЬЕВ ДЕНИСА И МИХАЙЛА КЫЗЪЮРОВЫХ
    # -------------------------------------------------------------
    # Создаем покойного отца Фёдора Кызъюрова (I431)
    if "I431" not in persons_by_id:
        p_i431 = {
            "id": "I431",
            "name": "Фёдор /Кызъюров/",
            "givn": "Фёдор",
            "surn": "Кызъюров",
            "sex": "M",
            "birt_date": "ок. 1762",
            "deat_date": "до 1811",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 9,
            "fams": ["F152"],
            "famc": None,
            "notes": ["Отец крестьян д. Ибской Дениса и Михайла (стрелка ополчения 1812 г.) Кызъюровых."],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        }
        persons.append(p_i431)
        persons_by_id["I431"] = p_i431

    # Связываем Дениса (I430) и Михайла (I414)
    if "I430" in persons_by_id:
        persons_by_id["I430"]["famc"] = "F152"
    if "I414" in persons_by_id:
        persons_by_id["I414"]["famc"] = "F152"

    if "F152" not in families_by_id:
        f152 = {
            "id": "F152",
            "husb": "I431",
            "wife": None,
            "children": ["I430", "I414"]
        }
        families.append(f152)
        families_by_id["F152"] = f152
    else:
        families_by_id["F152"]["children"] = ["I430", "I414"]

    # -------------------------------------------------------------
    # 3. ДВОР № 167: СЕМЬЯ ИЗЪЮРОВЫХ (КЫЗЪЮРОВЫХ)
    # -------------------------------------------------------------
    new_yard167_persons = [
        # Осип Афанасьевич Изъюров
        {
            "id": "I432",
            "name": "Осип Афанасьевич /Изъюров/",
            "givn": "Осип Афанасьевич",
            "surn": "Изъюров",
            "sex": "M",
            "birt_date": "ок. 1742",
            "deat_date": "1812",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 10,
            "fams": ["F153"],
            "famc": None,
            "notes": [
                "Крестьянин д. Ибской, глава двора № 167 по 7-й ревизии 1816 года (ГАВО, ф. 388, оп. 9, д. 201, л. 446 об.).",
                "По ревизии 1811 года — 69 лет, умер в 1812 году (род. ок. 1742 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        },
        # Фёдор Осипович Изъюров
        {
            "id": "I433",
            "name": "Фёдор Осипович /Изъюров/",
            "givn": "Фёдор Осипович",
            "surn": "Изъюров",
            "sex": "M",
            "birt_date": "ок. 1776",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 9,
            "fams": ["F154"],
            "famc": "F153",
            "notes": [
                "Сын Осипа Афанасьевича Изъюрова.",
                "В 7-й ревизии 1816 г. (двор № 167, л. 446 об.): 40 лет (в 1811 г. — 36 лет, род. ок. 1776 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        },
        # Марья Изъюрова (жена Фёдора)
        {
            "id": "I434",
            "name": "Марья /Изъюрова/",
            "givn": "Марья",
            "surn": "Изъюрова",
            "sex": "F",
            "birt_date": "ок. 1778",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 9,
            "fams": ["F154"],
            "famc": None,
            "notes": [
                "Жена Фёдора Осиповича Изъюрова.",
                "В 7-й ревизии 1816 г. (двор № 167, л. 447): 38 лет (род. ок. 1778 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        },
        # Федосья Осиповна Изъюрова (сестра Фёдора)
        {
            "id": "I435",
            "name": "Федосья Осиповна /Изъюрова/",
            "givn": "Федосья Осиповна",
            "surn": "Изъюрова",
            "sex": "F",
            "birt_date": "ок. 1791",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 9,
            "fams": [],
            "famc": "F153",
            "notes": [
                "Дочь Осипа Афанасьевича Изъюрова, сестра Фёдора.",
                "В 7-й ревизии 1816 г. (двор № 167, л. 447): 25 лет (род. ок. 1791 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        },
        # Иван Фёдорович Изъюров (сын Фёдора)
        {
            "id": "I436",
            "name": "Иван Фёдорович /Изъюров/",
            "givn": "Иван Фёдорович",
            "surn": "Изъюров",
            "sex": "M",
            "birt_date": "ок. 1807",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F154",
            "notes": [
                "Сын Фёдора Осиповича и Марьи Изъюровых.",
                "В 7-й ревизии 1816 г. (двор № 167, л. 446 об.): 9 лет (в 1811 г. — 5 лет, род. ок. 1807 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        },
        # Анна Фёдоровна Изъюрова (дочь Фёдора)
        {
            "id": "I437",
            "name": "Анна Фёдоровна /Изъюрова/",
            "givn": "Анна Фёдоровна",
            "surn": "Изъюрова",
            "sex": "F",
            "birt_date": "ок. 1814",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F154",
            "notes": [
                "Дочь Фёдора Осиповича и Марьи Изъюровых.",
                "В 7-й ревизии 1816 г. (двор № 167, л. 447): 2 года (род. ок. 1814 г.)."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        }
    ]

    for p in new_yard167_persons:
        if p["id"] not in persons_by_id:
            persons.append(p)
            persons_by_id[p["id"]] = p

    # Создаем союзы F153 и F154
    if "F153" not in families_by_id:
        f153 = {
            "id": "F153",
            "husb": "I432",
            "wife": None,
            "children": ["I433", "I435"]
        }
        families.append(f153)
        families_by_id["F153"] = f153

    if "F154" not in families_by_id:
        f154 = {
            "id": "F154",
            "husb": "I433",
            "wife": "I434",
            "children": ["I436", "I437"]
        }
        families.append(f154)
        families_by_id["F154"] = f154

    # Обновляем документ по Ибской (дворы 166 и 167)
    all_ibskaya_pids = ["I414", "I430", "I431", "I432", "I433", "I434", "I435", "I436", "I437"]
    for d in docs:
        if d["id"] == "revision_1816_ibskaya_opolchenets_166":
            d["title"] = "7-я ревизия 1816 г.: Деревня Ибская — Кызъюровы / Изъюровы (дворы № 166 и 167, лл. 446 об. – 447)"
            d["badge"] = "7-я ревизия (Ибская, лл. 446 об. – 447)"
            d["archive"] = "ГАВО, фонд 388, опись 9, дело 201, лл. 446 об. – 447 (дворы № 166 и 167)"
            d["personIds"] = all_ibskaya_pids
            d["desc"] = (
                "Подлинная запись 7-й ревизии 1816 года по деревне Ибской (ГАВО, ф. 388, оп. 9, д. 201, лл. 446 об. – 447):\n"
                "• Двор № 166: глава двора Денисъ Федоровъ Кызъюровъ; его братъ Михайло Федоровъ (23 года) — «Быль въ стрѣлкахъ въ ратникахъ» (участник Отечественной войны 1812 года в составе Вологодского ополчения).\n"
                "• Двор № 167: глава дома Осипъ Афанасьевъ Изъюровъ (69 лет в 1811 г., умер в 1812 г.); сын его Федоръ (40 лет), жена Федора Марья (38 лет), сын Федора Иванъ (9 лет), дочь Анна (2 года); сестра Федора Федосья (25 лет)."
            )

    sources_data["documents"] = docs

    # Сохраняем файлы data/
    with open(PERSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)
    with open(FAMILIES_FILE, "w", encoding="utf-8") as f:
        json.dump(families, f, ensure_ascii=False, indent=2)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_data, f, ensure_ascii=False, indent=2)

    # Обновляем archive_catalog.py
    # Заменяем в archive_catalog.py DOCS_CATALOG
    # Мы можем перезаписать DOCS_CATALOG в archive_catalog.py на основе sources_data['documents']
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        cat_content = f.read()

    # Заменяем блок DOCS_CATALOG = [...] на обновленный
    import pprint
    docs_formatted = json.dumps(docs, ensure_ascii=False, indent=2)
    # Находим границы DOCS_CATALOG = [ ... ]
    start_idx = cat_content.find("DOCS_CATALOG = [")
    end_idx = cat_content.find("\nPDF_ALBUMS = [")
    if start_idx != -1 and end_idx != -1:
        new_cat = cat_content[:start_idx] + "DOCS_CATALOG = " + docs_formatted + "\n" + cat_content[end_idx:]
        with open(CATALOG_FILE, "w", encoding="utf-8") as f:
            f.write(new_cat)
        print("Каталог archive_catalog.py синхронизирован.")

    print(f"Готово! Персон: {len(persons)}, Семей: {len(families)}, Документов: {len(docs)}")

if __name__ == "__main__":
    main()
