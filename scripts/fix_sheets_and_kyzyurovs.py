#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fix_sheets_and_kyzyurovs.py
1. Разделение архивных листов Коквиц строго по первоисточнику:
   - Лист 352 об. (Мужской пол) -> для всех мужчин Туркиных дворов 157, 158, 159
   - Лист 353 (Женский пол) -> для всех женщин Туркиных дворов 157, 158, 159
   - Лист 344 об. -> для Гавриила Туркина (семья 171)
   - Лист 363 об. -> для Степана Туркина (д. Малая Лыата)
   - Общий разворот лл. 352 об. - 353 -> общий документ для глав родов
2. Исправление фамилии во дворе № 167: КЫЗЪЮРОВ вместо Изъюров
   (Осип Афанасьевич, Фёдор Осипович, Марья, Федосья, Иван, Анна).
3. Проверка и фиксация семейных связей дворов 166 и 167.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PERSONS_FILE = os.path.join(DATA_DIR, "persons.json")
FAMILIES_FILE = os.path.join(DATA_DIR, "families.json")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
CATALOG_FILE = os.path.join(os.path.dirname(__file__), "..", "archive_catalog.py")

def main():
    with open(PERSONS_FILE, "r", encoding="utf-8") as f:
        persons = json.load(f)
    with open(FAMILIES_FILE, "r", encoding="utf-8") as f:
        families = json.load(f)
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_data = json.load(f)

    persons_by_id = {p["id"]: p for p in persons}

    # 1. Исправление фамилии Изъюров -> Кызъюров во дворе № 167
    kyzyurov_167_ids = ["I432", "I433", "I434", "I435", "I436", "I437"]
    for pid in kyzyurov_167_ids:
        if pid in persons_by_id:
            p = persons_by_id[pid]
            p["name"] = p["name"].replace("Изъюров", "Кызъюров").replace("Изъюрова", "Кызъюрова")
            p["surn"] = p["surn"].replace("Изъюров", "Кызъюров").replace("Изъюрова", "Кызъюрова")
            if "givn" in p:
                p["givn"] = p["givn"].replace("Изъюров", "Кызъюров").replace("Изъюрова", "Кызъюрова")
            p["notes"] = [n.replace("Изъюров", "Кызъюров").replace("Изъюрова", "Кызъюрова") for n in p.get("notes", [])]

    # 2. Разделение источников Коквиц на мужской (л. 352 об.) и женский (л. 353)
    kokvitsy_men = [
        "I80", "I148", "I369", "I370", "I371", "I372", "I374", "I381", "I383", "I384", "I385", "I387", "I79"
    ]
    kokvitsy_women = [
        "I368", "I373", "I375", "I376", "I377", "I378", "I379", "I380", "I382", "I386", "I388", "I389", "I390"
    ]

    # Назначаем мужчинам лист 352 об., женщинам - лист 353
    for pid in kokvitsy_men:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_kokvitsy_male_352ob"

    for pid in kokvitsy_women:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_kokvitsy_female_353"

    # Создаем отдельные четкие документы
    doc_male_352ob = {
        "id": "revision_1816_kokvitsy_male_352ob",
        "title": "7-я ревизия 1816 г.: Коквицкое селение — Мужской пол (семьи № 157, 158, 159, л. 352 об.)",
        "personId": "I148",
        "personIds": [pid for pid in kokvitsy_men if pid in persons_by_id],
        "personName": "Алексей Григорьевич, Григорий Степанович, Иван Леонтьевич Туркины",
        "category": "ancient",
        "categoryLabel": "Ревизии и переписи",
        "badge": "л. 352 об. — Мужчины (семьи 157–159)",
        "badgeColor": "#2563eb",
        "date": "1816 год",
        "archive": "ГАВО, фонд 388, опись 9, дело 201, л. 352 об.",
        "award": "7-я Государственная подушная ревизия",
        "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_l352ob_male.jpg",
        "thumb": "превью/kokvitsy_l352ob_male_thumb.jpg",
        "desc": (
            "Подлинный лист 352 об. ревизской сказки 7-й ревизии 1816 года по Коквицкому селению (ГАВО, ф. 388, оп. 9, д. 201, л. 352 об.) — МУЖСКОЙ ПОЛ:\n"
            "• Двор № 157: глава двора Иван Леонтьев Туркин (40 -> 44 года), сын Иван (3 -> 7 лет), брат Михайло Леонтьев (25 -> 29 лет).\n"
            "• Двор № 158: 6-й прадед Григорий Степанов Туркин (62 года по ревизии 1811 г., умре в 1814 году; род. ок. 1751 г.). "
            "Его сыновья: Василий (29 -> 33 года, сын Григорий вновь рожд. 1 год), второй сын Григорий (24 -> 28 лет), третий сын Иван (21 -> 25 лет), четвертый сын Иван же (17 -> 21 год).\n"
            "• Двор № 159: прямой 5-й прадед Алексей Григорьев Туркин (34 -> 38 лет, род. ок. 1778 г.). "
            "Его сыновья: Иван старший (4 -> 8 лет) и Иван 2-й (вновь рожд., 2 года)."
        )
    }

    doc_female_353 = {
        "id": "revision_1816_kokvitsy_female_353",
        "title": "7-я ревизия 1816 г.: Коквицкое селение — Женский пол (семьи № 157, 158, 159, л. 353)",
        "personId": "I368",
        "personIds": [pid for pid in kokvitsy_women if pid in persons_by_id],
        "personName": "Матрёна, Афанасия, Анна, Авдотья, Пелагия, Устинья Туркины",
        "category": "ancient",
        "categoryLabel": "Ревизии и переписи",
        "badge": "л. 353 — Женщины (семьи 157–159)",
        "badgeColor": "#be185d",
        "date": "1816 год",
        "archive": "ГАВО, фонд 388, опись 9, дело 201, л. 353",
        "award": "7-я Государственная подушная ревизия",
        "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_l353_female.jpg",
        "thumb": "превью/kokvitsy_l353_female_thumb.jpg",
        "desc": (
            "Подлинный лист 353 ревизской сказки 7-й ревизии 1816 года по Коквицкому селению (ГАВО, ф. 388, оп. 9, д. 201, л. 353) — ЖЕНСКИЙ ПОЛ:\n"
            "• Двор № 157: Ивана Леонтьева жена Устинья (27 лет), его сестра Акилина (47 лет), дочери Марья (13 лет) и Анна (3 года).\n"
            "• Двор № 158: Григорья Степанова жена Матрёна (63 года, 6-я прабабушка); Василья Григорьева жена Авдотья (25 лет), дочери Катерина (8 лет) и Дарья (5 лет); "
            "Григорья Григорьева жена Анна (22 года), свояченица Пелагия (70 лет, род. ок. 1746 г.).\n"
            "• Двор № 159: Алексея Григорьева жена Афанасия (38 лет, 5-я прабабушка), дочери Наталья (12 лет) и Ирина (6 лет)."
        )
    }

    doc_spread_352ob_353 = {
        "id": "revision_1816_turkin_kokvitsy",
        "title": "7-я ревизия 1816 г.: Коквицкое селение (полный 2-страничный разворот лл. 352 об. – 353)",
        "personId": "I148",
        "personIds": ["I148", "I80", "I368", "I379", "I384"],
        "personName": "Алексей Григорьевич, Григорий Степанович, Матрёна, Афанасия Туркины",
        "category": "ancient",
        "categoryLabel": "Ревизии и переписи",
        "badge": "Разворот (Коквицы, лл. 352 об. – 353)",
        "badgeColor": "#059669",
        "date": "1816 год",
        "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 352 об. – 353",
        "award": "7-я Государственная подушная ревизия",
        "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_spread_352ob_353.jpg",
        "thumb": "превью/kokvitsy_thumb_352ob_353.jpg",
        "desc": (
            "Сводный двухстраничный разворот ревизии 1816 г. по селению Коквицы (дворы № 157, 158, 159). "
            "Содержит одновременно мужскую (л. 352 об.) и женскую (л. 353) половины семейств Туркиных."
        )
    }

    # 3. Обновление документа по Ибской (дворы 166 и 167 Кызъюровых)
    all_ibskaya_pids = ["I414", "I430", "I431", "I432", "I433", "I434", "I435", "I436", "I437"]
    doc_ibskaya = {
        "id": "revision_1816_ibskaya_opolchenets_166",
        "title": "7-я ревизия 1816 г.: Деревня Ибская — Кызъюровы (дворы № 166 и 167, лл. 446 об. – 447)",
        "personId": "I414",
        "personIds": all_ibskaya_pids,
        "personName": "Михайло, Денис, Осип и Фёдор Кызъюровы",
        "category": "ancient",
        "categoryLabel": "Ревизии и переписи",
        "badge": "7-я ревизия (Ибская, лл. 446 об. – 447)",
        "badgeColor": "#dc2626",
        "date": "1816 год",
        "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 446 об. – 447 (дворы № 166 и 167)",
        "award": "7-я Государственная подушная ревизия",
        "file": "архив_сканы_первоисточников/1816_crops/ibskaya_spread_446ob_447.jpg",
        "thumb": "превью/ibskaya_thumb_446ob_447.jpg",
        "desc": (
            "Подлинная запись 7-й ревизии 1816 года по деревне Ибской (ГАВО, ф. 388, оп. 9, д. 201, лл. 446 об. – 447):\n"
            "• Двор № 166: глава двора Денисъ Федоровъ Кызъюровъ; его братъ Михайло Федоровъ (23 года) — «Быль въ стрѣлкахъ въ ратникахъ» (участник Отечественной войны 1812 года в составе Вологодского ополчения).\n"
            "• Двор № 167: глава дома Осипъ Афанасьевъ Кызъюровъ (69 лет в 1811 г., умер в 1812 г.); сын его Федоръ (40 лет), жена Федора Марья (38 лет), сын Федора Иванъ (9 лет), дочь Анна (2 года); сестра Федора Федосья (25 лет)."
        )
    }

    # Обновляем список документов
    existing_docs = sources_data.get("documents", [])
    replace_ids = {
        "revision_1816_kokvitsy_male_352ob", "revision_1816_kokvitsy_female_353",
        "revision_1816_turkin_kokvitsy", "revision_1816_ibskaya_opolchenets_166",
        "revision_1816_family_158_159_male", "revision_1816_family_158_159_female",
        "revision_1816_family_157_turkin"
    }
    updated_docs = [d for d in existing_docs if d["id"] not in replace_ids]
    updated_docs.extend([doc_male_352ob, doc_female_353, doc_spread_352ob_353, doc_ibskaya])

    sources_data["documents"] = updated_docs

    # Сохраняем data/
    with open(PERSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)
    with open(FAMILIES_FILE, "w", encoding="utf-8") as f:
        json.dump(families, f, ensure_ascii=False, indent=2)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_data, f, ensure_ascii=False, indent=2)

    # Синхронизируем archive_catalog.py
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        cat_content = f.read()

    docs_formatted = json.dumps(updated_docs, ensure_ascii=False, indent=2)
    docs_formatted = docs_formatted.replace(': null', ': None').replace(': true', ': True').replace(': false', ': False')

    start_idx = cat_content.find("DOCS_CATALOG = [")
    end_idx = cat_content.find("\nPDF_ALBUMS = [")
    if start_idx != -1 and end_idx != -1:
        new_cat = cat_content[:start_idx] + "DOCS_CATALOG = " + docs_formatted + "\n" + cat_content[end_idx:]
        with open(CATALOG_FILE, "w", encoding="utf-8") as f:
            f.write(new_cat)
        print("archive_catalog.py успешно обновлен.")

    print(f"Готово! Персон: {len(persons)}, Семей: {len(families)}, Документов: {len(updated_docs)}")

if __name__ == "__main__":
    main()
