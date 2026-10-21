#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/update_1816_user_corrections.py
Внесение проверенных пользователем правок по 7-й ревизии 1816 года:
1. Исправление поля birth_date -> birt_date для всех персон 1816 г. (I394–I418).
2. Замена раздельных сканов Коквицы на объединенный двухстраничный разворот (лл. 352об – 353).
3. Перенос Степана Туркина (I391, д. Малая Лыата) из активного древа в архив боковых персон (collateral_turkins.json).
4. Отвязка ошибочного источника от Марьи Туркиной 1794 (I392) и Еноха Гавриловича (I393), сомнение по имени Еноха.
5. Исправление сына Степана Поздеева: Ефим вместо Сергей (I407).
6. Исправление жены Ивана Поздеева: Елисавета вместо Капитолина (I406), добавление дочерей Анны и Феодосии.
7. Добавление дочерей Ивана Яковлевича Шуктомова и Ульяны (Ксения, Пелагея, Олена, Парасковья).
8. Добавление семьи Петра Ивановича Полещикова (жена Анна, сын Михаил, дочь Настасья).
9. Добавление сыновей Агафона Каракчиева (Василий 1803 г.р., ум. 1813, и незаконнорожденный сын Аверкий).
10. Добавление Дениса Федоровича Кызъюрова (брат Михайла, двор 166).
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PERSONS_FILE = os.path.join(DATA_DIR, "persons.json")
FAMILIES_FILE = os.path.join(DATA_DIR, "families.json")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
COORDS_FILE = os.path.join(DATA_DIR, "calibrated_coords.json")
COLLATERAL_FILE = os.path.join(DATA_DIR, "collateral_turkins.json")
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
    with open(COLLATERAL_FILE, "r", encoding="utf-8") as f:
        collateral = json.load(f)

    persons_by_id = {p["id"]: p for p in persons}
    families_by_id = {f["id"]: f for f in families}

    # 1. Исправление birth_date -> birt_date для всех персон 1816 г.
    for p in persons:
        if "birth_date" in p:
            val = p.pop("birth_date").replace(" г.", "").strip()
            p["birt_date"] = val
        if "residence" in p:
            res = p.pop("residence")
            if not p.get("birt_plac"):
                p["birt_plac"] = f"{res}, Яренский уезд, Вологодская губерния"
        if not p.get("gen"):
            # Вычисление поколения по году рождения
            bdate = p.get("birt_date", "")
            import re
            m = re.search(r"\b(1\d{3}|20\d{2})\b", str(bdate))
            if m:
                yr = int(m.group(1))
                p["gen"] = max(1, min(15, round((1995 - yr) / 30) + 1))
            else:
                p["gen"] = 8

    # 2. Перенос Степана Туркина (I391) в collateral_turkins.json
    stepan_i391 = persons_by_id.get("I391")
    if stepan_i391:
        # Проверяем наличие секции 1816 в collateral_turkins.json
        sec_1816 = next((s for s in collateral.get("sections", []) if s.get("section_id") == "revision_1816"), None)
        if not sec_1816:
            sec_1816 = {
                "section_id": "revision_1816",
                "title": "Боковые семьи Туркиных по 7-й ревизии 1816 г. (Яренский уезд)",
                "description": "Персоналии рода Туркиных по 7-й ревизии 1816 года, не входящие в прямое древо пробанда.",
                "persons": []
            }
            collateral.setdefault("sections", []).append(sec_1816)
        
        # Добавляем Степана
        sec_1816["persons"].append({
            "id": stepan_i391["id"],
            "name": stepan_i391["name"],
            "birt_date": stepan_i391.get("birt_date", "ок. 1780"),
            "deat_date": stepan_i391.get("deat_date", "после 1812"),
            "birt_plac": stepan_i391.get("birt_plac", "д. Малая Лыата, Коквицкое селение"),
            "notes": stepan_i391.get("notes", [])
        })
        collateral["total_persons"] = sum(len(s.get("persons", [])) for s in collateral["sections"])
        
        # Удаляем из persons и coords
        persons = [p for p in persons if p["id"] != "I391"]
        coords.pop("I391", None)
        persons_by_id.pop("I391", None)
        print("I391 (Степан Туркин) перенесен в архив боковых ветвей (collateral_turkins.json).")

    # 3. Марья Туркина 1794 (I392) и Енох Гаврилович (I393) - отвязка неподходящего источника
    if "I392" in persons_by_id:
        p_i392 = persons_by_id["I392"]
        p_i392["source_id"] = None
        p_i392["notes"].append("Архивный скан л. 345 (вдова Марья 22 лет) находится в обработке.")

    if "I393" in persons_by_id:
        p_i393 = persons_by_id["I393"]
        p_i393["name"] = "Енох (?) Гаврилович /Туркин/"
        p_i393["givn"] = "Енох (?) Гаврилович"
        p_i393["source_id"] = None
        p_i393["notes"].append("Имя предположительно прочитано как Енох (?). Рукописный почерк ревизии неразборчив, требуется сверка по метрическим книгам за 1813–1814 гг.")

    # 4. Исправление Степана Поздеева сына: Ефим (I407)
    if "I407" in persons_by_id:
        p_i407 = persons_by_id["I407"]
        p_i407["name"] = "⚔️ Ефим Степанович /Поздеев/"
        p_i407["givn"] = "Ефим Степанович"
        p_i407["surn"] = "Поздеев"
        p_i407["notes"] = [
            "Сын Степана Андреевича и Парасковьи Поздеевых.",
            "Участник Заграничного похода русской армии 1813 года против Наполеона.",
            "В 7-й ревизии 1816 г. (двор № 200, л. 452 об.): 'сынъ Ефимъ — по ревизии 1811 г. 16 лет, Рекрутъ въ 1813 году' (род. ок. 1795-1796 г.)."
        ]

    # 5. Исправление жены Ивана Поздеева: Елисавета (I406)
    if "I406" in persons_by_id:
        p_i406 = persons_by_id["I406"]
        p_i406["name"] = "Елисавета /Поздеева/"
        p_i406["givn"] = "Елисавета"
        p_i406["surn"] = "Поздеева"
        p_i406["birt_date"] = "ок. 1785"
        p_i406["notes"] = [
            "Жена Ивана Степановича Поздеева.",
            "Зафиксирована в 7-й ревизии 1816 года (двор № 200, л. 453): 'Ивана жена Елисавета — 31 год' (род. ок. 1785 г.)."
        ]

    # 6. Добавление дочерей Ивана Степановича Поздеева: Анна и Феодосия
    new_daughters_pozdeev = [
        {
            "id": "I423",
            "name": "Анна Ивановна /Поздеева/",
            "givn": "Анна Ивановна",
            "surn": "Поздеева",
            "sex": "F",
            "birt_date": "ок. 1814",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F148",
            "notes": ["Дочь Ивана Степановича и Елисаветы Поздеевых. В 7-й ревизии 1816 г. (двор № 200, л. 453) — 2 года."],
            "source_id": "revision_1816_erozdino_pozdeev_200",
            "is_new_1816": True
        },
        {
            "id": "I424",
            "name": "Феодосия Ивановна /Поздеева/",
            "givn": "Феодосия Ивановна",
            "surn": "Поздеева",
            "sex": "F",
            "birt_date": "ок. 1815",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F148",
            "notes": ["Дочь Ивана Степановича и Елисаветы Поздеевых. В 7-й ревизии 1816 г. (двор № 200, л. 453) — 1 год."],
            "source_id": "revision_1816_erozdino_pozdeev_200",
            "is_new_1816": True
        }
    ]
    for d in new_daughters_pozdeev:
        if d["id"] not in persons_by_id:
            persons.append(d)
            persons_by_id[d["id"]] = d
            if d["id"] not in families_by_id["F148"].get("children", []):
                families_by_id["F148"].setdefault("children", []).append(d["id"])

    # 7. Добавление дочерей Ивана Яковлевича Шуктомова (двор 204)
    new_daughters_shuktomov = [
        {
            "id": "I419",
            "name": "Ксения Ивановна /Шуктомова/",
            "givn": "Ксения Ивановна",
            "surn": "Шуктомова",
            "sex": "F",
            "birt_date": "ок. 1796",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F146",
            "notes": ["Дочь Ивана Яковлевича и Ульяны Шуктомовых. В 7-й ревизии 1816 г. (двор № 204, л. 454) — 20 лет."],
            "source_id": "revision_1816_erozdino_shuktomov_recruits_204",
            "is_new_1816": True
        },
        {
            "id": "I420",
            "name": "Пелагея Ивановна /Шуктомова/",
            "givn": "Пелагея Ивановна",
            "surn": "Шуктомова",
            "sex": "F",
            "birt_date": "ок. 1806",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F146",
            "notes": ["Дочь Ивана Яковлевича и Ульяны Шуктомовых. В 7-й ревизии 1816 г. (двор № 204, л. 454) — 10 лет."],
            "source_id": "revision_1816_erozdino_shuktomov_recruits_204",
            "is_new_1816": True
        },
        {
            "id": "I421",
            "name": "Олена Ивановна /Шуктомова/",
            "givn": "Олена Ивановна",
            "surn": "Шуктомова",
            "sex": "F",
            "birt_date": "ок. 1808",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F146",
            "notes": ["Дочь Ивана Яковлевича и Ульяны Шуктомовых. В 7-й ревизии 1816 г. (двор № 204, л. 454) — 8 лет."],
            "source_id": "revision_1816_erozdino_shuktomov_recruits_204",
            "is_new_1816": True
        },
        {
            "id": "I422",
            "name": "Парасковья Ивановна /Шуктомова/",
            "givn": "Парасковья Ивановна",
            "surn": "Шуктомова",
            "sex": "F",
            "birt_date": "ок. 1810",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": "F146",
            "notes": ["Дочь Ивана Яковлевича и Ульяны Шуктомовых. В 7-й ревизии 1816 г. (двор № 204, л. 454) — 6 лет."],
            "source_id": "revision_1816_erozdino_shuktomov_recruits_204",
            "is_new_1816": True
        }
    ]
    for d in new_daughters_shuktomov:
        if d["id"] not in persons_by_id:
            persons.append(d)
            persons_by_id[d["id"]] = d
            if d["id"] not in families_by_id["F146"].get("children", []):
                families_by_id["F146"].setdefault("children", []).append(d["id"])

    # 8. Добавление семьи Петра Ивановича Полещикова (I411)
    new_poleshchikov = [
        {
            "id": "I425",
            "name": "Анна /Полещикова/",
            "givn": "Анна",
            "surn": "Полещикова",
            "sex": "F",
            "birt_date": "ок. 1794",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 8,
            "fams": ["F151"],
            "famc": None,
            "notes": ["Жена Петра Ивановича Полещикова. В 7-й ревизии 1816 г. (двор № 195, л. 452) — 22 года (род. ок. 1794 г.)."],
            "source_id": "revision_1816_erozdino_poleshchikov_195",
            "is_new_1816": True
        },
        {
            "id": "I426",
            "name": "Михаил Петрович /Полещиков/",
            "givn": "Михаил Петрович",
            "surn": "Полещиков",
            "sex": "M",
            "birt_date": "ок. 1815",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 7,
            "fams": [],
            "famc": "F151",
            "notes": ["Сын Петра Ивановича и Анны Полещиковых. В 7-й ревизии 1816 г. (двор № 195, л. 451 об.) — 1 год (род. ок. 1815 г.)."],
            "source_id": "revision_1816_erozdino_poleshchikov_195",
            "is_new_1816": True
        },
        {
            "id": "I427",
            "name": "Настасья Петровна /Полещикова/",
            "givn": "Настасья Петровна",
            "surn": "Полещикова",
            "sex": "F",
            "birt_date": "ок. 1815",
            "birt_plac": "д. Ероздинская, Ляльские селения",
            "gen": 7,
            "fams": [],
            "famc": "F151",
            "notes": ["Дочь Петра Ивановича и Анны Полещиковых. В 7-й ревизии 1816 г. (двор № 195, л. 452) — 1 год (род. ок. 1815 г.)."],
            "source_id": "revision_1816_erozdino_poleshchikov_195",
            "is_new_1816": True
        }
    ]
    for p in new_poleshchikov:
        if p["id"] not in persons_by_id:
            persons.append(p)
            persons_by_id[p["id"]] = p

    # Добавляем союз F151
    if "F151" not in families_by_id:
        f151 = {
            "id": "F151",
            "husb": "I411",
            "wife": "I425",
            "children": ["I426", "I427"]
        }
        families.append(f151)
        families_by_id["F151"] = f151
    if "I411" in persons_by_id:
        if "F151" not in persons_by_id["I411"].get("fams", []):
            persons_by_id["I411"].setdefault("fams", []).append("F151")

    # 9. Добавление сыновей Агафона Никифоровича Каракчиева (двор 15): Василий и Аверкий
    new_karakchievs = [
        {
            "id": "I428",
            "name": "Василий Агафонович /Каракчиев/",
            "givn": "Василий Агафонович",
            "surn": "Каракчиев",
            "sex": "M",
            "birt_date": "ок. 1803",
            "deat_date": "1813",
            "birt_plac": "Погост Ляльский, Яренский уезд",
            "gen": 8,
            "fams": [],
            "famc": "F150",
            "notes": ["Сын Агафона Никифоровича и Парасковьи Каракчиевых, брат Ионы. В ревизии 1816 г. (двор № 15): '8 лет в 1811 г., умре в 1813 году'."],
            "source_id": "revision_1816_lyali_karakchiev_15",
            "is_new_1816": True
        },
        {
            "id": "I429",
            "name": "Аверкий /Каракчиев/",
            "givn": "Аверкий",
            "surn": "Каракчиев",
            "sex": "M",
            "birt_date": "ок. 1812",
            "birt_plac": "Погост Ляльский, Яренский уезд",
            "gen": 8,
            "fams": [],
            "famc": "F150",
            "notes": ["Незаконнорожденный сын при семье Агафона Никифоровича Каракчиева по 7-й ревизии 1816 года (двор № 15)."],
            "source_id": "revision_1816_lyali_karakchiev_15",
            "is_new_1816": True
        }
    ]
    for p in new_karakchievs:
        if p["id"] not in persons_by_id:
            persons.append(p)
            persons_by_id[p["id"]] = p
            if p["id"] not in families_by_id["F150"].get("children", []):
                families_by_id["F150"].setdefault("children", []).append(p["id"])

    # 10. Добавление Дениса Федоровича Кызъюрова (брат ополченца Михайла, двор 166)
    if "I430" not in persons_by_id:
        p_i430 = {
            "id": "I430",
            "name": "Денис Федорович /Кызъюров/",
            "givn": "Денис Федорович",
            "surn": "Кызъюров",
            "sex": "M",
            "birt_date": "ок. 1788",
            "birt_plac": "д. Ибская, Ляльские селения",
            "gen": 8,
            "fams": [],
            "famc": None,
            "notes": [
                "Крестьянин д. Ибской, глава двора № 166 в 7-й ревизии 1816 г. (л. 446 об.).",
                "Старший брат ратника Вологодского ополчения Михайла Федоровича Кызъюрова."
            ],
            "source_id": "revision_1816_ibskaya_opolchenets_166",
            "is_new_1816": True
        }
        persons.append(p_i430)
        persons_by_id["I430"] = p_i430

    # 11. Обновление источников в sources_data: возвращаем Коквицы к полному 2-страничному развороту
    spread_file = "архив_сканы_первоисточников/1816_crops/kokvitsy_spread_352ob_353.jpg"
    spread_thumb = "превью/kokvitsy_thumb_352ob_353.jpg"

    for doc in sources_data.get("documents", []):
        if doc.get("id") in ["revision_1816_family_157_turkin", "revision_1816_family_158_159_male", "revision_1816_family_158_159_female"]:
            doc["file"] = spread_file
            doc["thumb"] = spread_thumb
            doc["badge"] = "7-я ревизия (Разворот Коквицы, лл. 352 об. – 353)"
            doc["badgeColor"] = "#2563eb"
            # Включаем всех персон Коквицких семей 157, 158, 159
            all_kokvitsy_pids = [
                "I148", "I80", "I81", "I79", "I368", "I369", "I370", "I371", "I372", "I373", "I374", "I375", "I376", "I377", "I378",
                "I379", "I380", "I381", "I382", "I383", "I384", "I385", "I386", "I387", "I388", "I389", "I390"
            ]
            doc["personIds"] = [pid for pid in all_kokvitsy_pids if pid in persons_by_id]
        
        # Обновляем personIds для Ероздинских документов
        if doc.get("id") == "revision_1816_erozdino_shuktomov_recruits_204":
            doc["personIds"] = ["I398", "I399", "I400", "I401", "I402", "I419", "I420", "I421", "I422"]
        if doc.get("id") == "revision_1816_erozdino_pozdeev_200":
            doc["personIds"] = ["I403", "I404", "I405", "I406", "I407", "I408", "I423", "I424", "I57", "I25"]
        if doc.get("id") == "revision_1816_erozdino_poleshchikov_195":
            doc["personIds"] = ["I409", "I410", "I411", "I412", "I413", "I425", "I426", "I427", "I353", "I354", "I55", "I37", "I24"]
        if doc.get("id") == "revision_1816_lyali_karakchiev_15":
            doc["personIds"] = ["I415", "I416", "I417", "I418", "I428", "I429", "I65", "I58", "I40", "I25"]
        if doc.get("id") == "revision_1816_ibskaya_opolchenets_166":
            doc["personIds"] = ["I414", "I430"]
        if doc.get("id") == "revision_1816_gavrilo_turkin_1813":
            # Убираем Марью и Еноха из ополченческого скана
            doc["personIds"] = ["I248"]

    # 12. Сохраняем файлы
    with open(PERSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)
    with open(FAMILIES_FILE, "w", encoding="utf-8") as f:
        json.dump(families, f, ensure_ascii=False, indent=2)
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources_data, f, ensure_ascii=False, indent=2)
    with open(COORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=2)
    with open(COLLATERAL_FILE, "w", encoding="utf-8") as f:
        json.dump(collateral, f, ensure_ascii=False, indent=2)

    # 13. Обновляем archive_catalog.py
    # Заменяем в archive_catalog.py описания и файлы Коквицы
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        cat_code = f.read()

    # Заменяем привязки kokvitsy_l352ob_male.jpg и kokvitsy_l353_female.jpg на разворот
    cat_code = cat_code.replace("архив_сканы_первоисточников/1816_crops/kokvitsy_l352ob_male.jpg", spread_file)
    cat_code = cat_code.replace("архив_сканы_первоисточников/1816_crops/kokvitsy_l353_female.jpg", spread_file)
    cat_code = cat_code.replace("превью/kokvitsy_l352ob_male_thumb.jpg", spread_thumb)
    cat_code = cat_code.replace("превью/kokvitsy_l353_female_thumb.jpg", spread_thumb)
    cat_code = cat_code.replace("л. 352 об. (мужчины 157-159)", "лл. 352 об. – 353 (Коквицы, семьи 157-159)")
    cat_code = cat_code.replace("л. 353 — женский пол (семьи 157–159)", "лл. 352 об. – 353 (Коквицы, семьи 157-159)")
    cat_code = cat_code.replace("Сергей (15 лет, «Рекрутъ въ 1813 году»)", "Ефим (16 лет, «Рекрутъ въ 1813 году»)")
    cat_code = cat_code.replace("жена Ивана Капитолина (31 год)", "жена Ивана Елисавета (31 год)")

    with open(CATALOG_FILE, "w", encoding="utf-8") as f:
        f.write(cat_code)

    print(f"Все изменения успешно записаны. Персон в базе: {len(persons)}, семей: {len(families)}")

if __name__ == "__main__":
    main()
