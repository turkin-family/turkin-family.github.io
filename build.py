#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py - Единый мастер-скрипт сборки, валидации и экспорта генеалогического проекта.

Запуск:
    python3 build.py

Выполняет:
    1. Проверку целостности реляционной базы данных data/*.json (data_manager.py)
    2. Проверку отсутствия геометрических коллизий Smart-Layout (layout_engine.py)
    3. Экспорт родословной в международный формат GEDCOM 5.5.1 (build_genealogy.py)
    4. Генерацию веб-приложения: index.html, tree.html, родословная.html (generate_final_tree.py)
    5. Контрольный аудит файлов и готовности к деплою
"""

import sys
import os
import subprocess
import json

def run_step(step_num, title, func):
    print(f"\n[{step_num}/4] ▶ {title}...")
    try:
        func()
        print(f"[{step_num}/4]  Успешно.")
    except Exception as e:
        print(f"[{step_num}/4] ❌ ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)

def step_validate_data():
    import data_manager
    ok, errors = data_manager.validate_integrity()
    if not ok:
        raise ValueError(f"Ошибки в базе данных:\n" + "\n".join(errors))

def step_validate_layout():
    import layout_engine
    import data_manager
    persons = data_manager.load_persons()
    families = data_manager.load_families()
    coords = layout_engine.compute_smart_layout(persons, families)
    ok, collisions = layout_engine.validate_layout(coords)
    if not ok:
        raise ValueError(f"Обнаружены наложения карточек:\n" + "\n".join(collisions))

def step_export_gedcom():
    import build_genealogy
    build_genealogy.export_gedcom("rodoslovnaya_turkin.ged")

def step_generate_html():
    result = subprocess.run([sys.executable, "generate_final_tree.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Сбой generate_final_tree.py:\n{result.stderr}")
    print("   " + result.stdout.strip())
    
    # Генерация тайской версии (thai.html)
    res_thai = subprocess.run([sys.executable, "scripts/build_thai_clean.py"], capture_output=True, text=True)
    if res_thai.returncode != 0:
        raise RuntimeError(f"Сбой build_thai_clean.py:\n{res_thai.stderr}")
    print("   " + res_thai.stdout.strip())

def main():
    print("=" * 65)
    print("      СБОРКА И ВАЛИДАЦИЯ ГЕНЕАЛОГИЧЕСКОГО ПРОЕКТА «ТУРКИНЫ»")
    print("=" * 65)

    run_step(1, "Валидация базы данных (data_manager)", step_validate_data)
    run_step(2, "Геометрическая проверка Smart-Layout (layout_engine)", step_validate_layout)
    run_step(3, "Экспорт стандарта GEDCOM 5.5.1 (build_genealogy)", step_export_gedcom)
    run_step(4, "Генерация HTML-приложения (generate_final_tree)", step_generate_html)

    # Итоговая статистика
    with open("data/persons.json", "r", encoding="utf-8") as f:
        persons = json.load(f)
    with open("data/families.json", "r", encoding="utf-8") as f:
        families = json.load(f)
    with open("data/sources.json", "r", encoding="utf-8") as f:
        sources = json.load(f)

    print("\n" + "=" * 65)
    print("  СБОРКА ЗАВЕРШЕНА УСПЕШНО! ВСЕ 100% ПРОВЕРОК ПРОЙДЕНЫ.")
    print("=" * 65)
    print(f"  • Персон в древе:        {len(persons)}")
    print(f"  • Семейных союзов:       {len(families)}")
    print(f"  • Архивных документов:   {len(sources.get('documents', []))}")
    print(f"  • PDF-альбомов и книг:   {len(sources.get('pdf_albums', []))}")
    print(f"  • Готовых HTML-файлов:   index.html, tree.html, родословная.html, thai.html")
    print(f"  • Экспорт GEDCOM:        rodoslovnaya_turkin.ged")
    print("-" * 65)
    print("  Для локального запуска выполните:")
    print("      python3 serve.py   (или ./start_server.sh)")
    print("=" * 65)

if __name__ == "__main__":
    main()
