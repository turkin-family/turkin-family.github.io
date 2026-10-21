#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_yard_spreads_kokvitsy.py

Назначает для каждого двора Туркиных в с. Коквицы (7-я ревизия 1816 г.)
свой отдельный двухстраничный склеенный разворот (МУЖ + ЖЕН):
- Двор № 157 -> revision_1816_turkin_157 (kokvitsy_yard_157_spread.jpg)
- Двор № 158 -> revision_1816_turkin_158 (kokvitsy_yard_158_spread.jpg)
- Двор № 159 -> revision_1816_turkin_159 (kokvitsy_yard_159_spread.jpg)

Обновляет data/sources.json, data/persons.json и archive_catalog.py.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
PERSONS_FILE = os.path.join(DATA_DIR, "persons.json")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
CATALOG_FILE = os.path.join(ROOT, "archive_catalog.py")

DOC_157 = {
    "id": "revision_1816_turkin_157",
    "title": "7-я ревизия 1816 г.: Семья Туркиных с. Коквицы (двор № 157, лл. 352 об. – 353)",
    "personId": "I384",
    "personIds": ["I384", "I385", "I386", "I387", "I388", "I389", "I390"],
    "personName": "Иван Леонтьевич Туркин и семья (двор № 157)",
    "category": "ancient",
    "categoryLabel": "Ревизии и переписи",
    "badge": "7-я ревизия (двор № 157, Коквицы)",
    "badgeColor": "#2563eb",
    "date": "1816 год",
    "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 352 об. – 353 (двор № 157)",
    "award": "7-я Государственная подушная ревизия",
    "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_yard_157_spread.jpg",
    "thumb": "превью/kokvitsy_yard_157_thumb.jpg",
    "desc": "Подлинная запись 7-й ревизии 1816 года по селению Коквицы (ГАВО, ф. 388, оп. 9, д. 201, лл. 352 об. – 353, двор № 157):\n• Мужской пол (л. 352 об.): глава двора Иванъ Леонтьевъ Туркинъ (по ревизии 1811 г. 40 лет, в 1816 г. — 44 года); сын его Иванъ (3 -> 7 лет); брат Ивана Михайло Леонтьевъ (25 -> 29 лет).\n• Женский пол (л. 353): жена Ивана Устинья (27 лет); дочери Акилина (17 лет), Марья (13 лет), Анна (9 лет)."
}

DOC_158 = {
    "id": "revision_1816_turkin_158",
    "title": "7-я ревизия 1816 г.: Семья Туркиных с. Коквицы (двор № 158, лл. 352 об. – 353)",
    "personId": "I80",
    "personIds": ["I80", "I368", "I369", "I370", "I371", "I372", "I373", "I374", "I375", "I376", "I377", "I378"],
    "personName": "Григорий Степанович Туркин и сыновья (двор № 158)",
    "category": "ancient",
    "categoryLabel": "Ревизии и переписи",
    "badge": "7-я ревизия (двор № 158, Коквицы)",
    "badgeColor": "#059669",
    "date": "1816 год",
    "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 352 об. – 353 (двор № 158)",
    "award": "7-я Государственная подушная ревизия",
    "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_yard_158_spread.jpg",
    "thumb": "превью/kokvitsy_yard_158_thumb.jpg",
    "desc": "Подлинная запись 7-й ревизии 1816 года по селению Коквицы (ГАВО, ф. 388, оп. 9, д. 201, лл. 352 об. – 353, двор № 158):\n• Мужской пол (л. 352 об.): Григорей Степановъ Туркинъ (по ревизии 1811 г. 62 года, умре в 1814 году; 6-й прадед). Сыновья его: Василей (29 -> 33 года); Василья сынъ Григорей (вновь рожд., 1 год); второй сынъ Григорей (24 -> 28 лет); третий сынъ Иванъ (21 -> 25 лет); четвертый сынъ Иванъ же (17 -> 21 год).\n• Женский пол (л. 353): Григорья Степанова жена Матрена (63 года, 6-я прабабушка); Василья Григорьева жена Авдотья (25 лет), дочери его Катерина (8 лет) и Дарья (5 лет); Григорья Григорьева жена Анна (22 года); свояченица его Пелагия (70 лет, род. ок. 1746 г.)."
}

DOC_159 = {
    "id": "revision_1816_turkin_159",
    "title": "7-я ревизия 1816 г.: Семья Туркиных с. Коквицы (двор № 159, лл. 352 об. – 353)",
    "personId": "I148",
    "personIds": ["I148", "I379", "I380", "I381", "I382", "I383"],
    "personName": "Алексей Григорьевич Туркин и семья (двор № 159)",
    "category": "ancient",
    "categoryLabel": "Ревизии и переписи",
    "badge": "7-я ревизия (двор № 159, Коквицы)",
    "badgeColor": "#7c3aed",
    "date": "1816 год",
    "archive": "ГАВО, фонд 388, опись 9, дело 201, лл. 352 об. – 353 (двор № 159)",
    "award": "7-я Государственная подушная ревизия",
    "file": "архив_сканы_первоисточников/1816_crops/kokvitsy_yard_159_spread.jpg",
    "thumb": "превью/kokvitsy_yard_159_thumb.jpg",
    "desc": "Подлинная запись 7-й ревизии 1816 года по селению Коквицы (ГАВО, ф. 388, оп. 9, д. 201, лл. 352 об. – 353, двор № 159):\n• Мужской пол (л. 352 об.): прямой 5-й прадед Алексѣй Григорьевъ Туркинъ (по ревизии 1811 г. 34 года, в 1816 г. — 38 лет; род. ок. 1778 г.). Сыновья его: Иванъ старший (4 -> 8 лет) и Иванъ 2-й (вновь рожд., 2 года).\n• Женский пол (л. 353): Алексѣя Григорьева жена Афанасія (38 лет, 5-я прабабушка); дочери его Наталья (12 лет) и Ирина (6 лет)."
}

def main():
    # 1. Обновление persons.json
    with open(PERSONS_FILE, "r", encoding="utf-8") as f:
        persons = json.load(f)

    persons_by_id = {p["id"]: p for p in persons}

    yard_157_pids = ["I384", "I385", "I386", "I387", "I388", "I389", "I390", "I79", "I81"]
    yard_158_pids = ["I80", "I368", "I369", "I370", "I371", "I372", "I373", "I374", "I375", "I376", "I377", "I378"]
    yard_159_pids = ["I148", "I379", "I380", "I381", "I382", "I383"]

    for pid in yard_157_pids:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_turkin_157"

    for pid in yard_158_pids:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_turkin_158"

    for pid in yard_159_pids:
        if pid in persons_by_id:
            persons_by_id[pid]["source_id"] = "revision_1816_turkin_159"

    with open(PERSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)
    print("Updated data/persons.json with yard-specific source_ids.")

    # 2. Обновление sources.json
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources_data = json.load(f)

    obsolete_ids = {
        "revision_1816_kokvitsy_male_352ob",
        "revision_1816_kokvitsy_female_353",
        "revision_1816_turkin_kokvitsy",
        "revision_1816_turkin_157",
        "revision_1816_turkin_158",
        "revision_1816_turkin_159"
    }

    docs = [d for d in sources_data["documents"] if d["id"] not in obsolete_ids]
    docs.extend([DOC_157, DOC_158, DOC_159])
    sources_data["documents"] = docs

    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_data, f, ensure_ascii=False, indent=2)
    print(f"Updated data/sources.json with 3 yard documents (total docs: {len(docs)}).")

    # 3. Обновление archive_catalog.py
    # Читаем существующий archive_catalog.py и заменяем DOCS_CATALOG
    # Преобразуем docs в красивый python-код
    def py_repr(val, indent_level=1):
        ind = "    " * indent_level
        if isinstance(val, dict):
            lines = ["{"]
            for k, v in val.items():
                lines.append(f"{ind}    {repr(k)}: {py_repr(v, indent_level + 1)},")
            lines.append(f"{ind}}}")
            return "\n".join(lines)
        elif isinstance(val, list):
            if all(isinstance(x, str) for x in val) and len(val) <= 12:
                return "[" + ", ".join(repr(x) for x in val) + "]"
            lines = ["["]
            for x in val:
                lines.append(f"{ind}    {py_repr(x, indent_level + 1)},")
            lines.append(f"{ind}]")
            return "\n".join(lines)
        elif val is None:
            return "None"
        elif isinstance(val, bool):
            return "True" if val else "False"
        else:
            return repr(val)

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        cat_code = f.read()

    # Сохраняем заголовок до DOCS_CATALOG = [
    prefix = cat_code[:cat_code.find("DOCS_CATALOG = [")]
    if not prefix:
        prefix = '"""\nКаталог архивных документов проекта Родословная Туркиных.\n"""\n\n'

    # Проверяем, есть ли что-то после списка документов
    # В archive_catalog.py DOCS_CATALOG и PDF_ALBUMS
    lines = [f"{prefix}DOCS_CATALOG = ["]
    for d in docs:
        lines.append(f"    {py_repr(d, 1)},")
    lines.append("]\n")

    lines.append("PDF_ALBUMS = [")
    for a in sources_data.get("pdf_albums", []):
        lines.append(f"    {py_repr(a, 1)},")
    lines.append("]\n")

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Updated archive_catalog.py (total docs: {len(docs)}, pdf_albums: {len(sources_data.get('pdf_albums', []))}).")

if __name__ == "__main__":
    main()
