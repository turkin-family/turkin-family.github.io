"""
data_manager.py - Единый модуль управления данными родословной Туркиных.
Хранит и валидирует реляционные данные:
  - data/persons.json
  - data/families.json
  - data/sources.json
  - data/evidence.json
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PERSONS_FILE = os.path.join(DATA_DIR, "persons.json")
FAMILIES_FILE = os.path.join(DATA_DIR, "families.json")
SOURCES_FILE = os.path.join(DATA_DIR, "sources.json")
EVIDENCE_FILE = os.path.join(DATA_DIR, "evidence.json")


def load_persons() -> List[Dict[str, Any]]:
    """Загрузить список всех персон из data/persons.json"""
    with open(PERSONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_persons(persons: List[Dict[str, Any]]) -> None:
    """Сохранить список персон в data/persons.json"""
    with open(PERSONS_FILE, "w", encoding="utf-8") as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)


def load_families() -> List[Dict[str, Any]]:
    """Загрузить список всех семей из data/families.json"""
    with open(FAMILIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_families(families: List[Dict[str, Any]]) -> None:
    """Сохранить список семей в data/families.json"""
    with open(FAMILIES_FILE, "w", encoding="utf-8") as f:
        json.dump(families, f, ensure_ascii=False, indent=2)


def load_sources() -> Dict[str, Any]:
    """Загрузить каталог архивных источников из data/sources.json"""
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sources(sources: Dict[str, Any]) -> None:
    """Сохранить каталог источников в data/sources.json"""
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)


def load_evidence() -> List[Dict[str, Any]]:
    """Загрузить реестр доказательств (evidence links)"""
    with open(EVIDENCE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_evidence(evidence: List[Dict[str, Any]]) -> None:
    """Сохранить реестр доказательств"""
    with open(EVIDENCE_FILE, "w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)


def validate_integrity() -> Tuple[bool, List[str]]:
    """
    Проверка ссылочной целостности базы данных:
    - Уникальность ID персон и семей
    - Существование всех husb, wife, children в persons
    - Соответствие personIds в sources
    """
    persons = load_persons()
    families = load_families()
    sources_data = load_sources()
    documents = sources_data.get("documents", [])
    
    errors = []
    
    # 1. Person IDs
    person_ids = set()
    for p in persons:
        pid = p.get("id")
        if not pid:
            errors.append("Персона без ID обнаружена!")
        elif pid in person_ids:
            errors.append(f"Дублирующийся ID персоны: {pid}")
        person_ids.add(pid)
        
    # 2. Family IDs & References
    family_ids = set()
    for f in families:
        fid = f.get("id")
        if not fid:
            errors.append("Семья без ID обнаружена!")
        elif fid in family_ids:
            errors.append(f"Дублирующийся ID семьи: {fid}")
        family_ids.add(fid)
        
        husb = f.get("husb")
        wife = f.get("wife")
        children = f.get("children", [])
        
        if husb and husb not in person_ids:
            errors.append(f"В семье {fid} муж {husb} отсутствует в persons!")
        if wife and wife not in person_ids:
            errors.append(f"В семье {fid} жена {wife} отсутствует в persons!")
        for c in children:
            if c not in person_ids:
                errors.append(f"В семье {fid} ребёнок {c} отсутствует в persons!")
                
    # 3. Source References
    for doc in documents:
        doc_id = doc.get("id", "UNKNOWN")
        p_ids = doc.get("personIds", [])
        if not p_ids and doc.get("personId"):
            p_ids = [doc.get("personId")]
        for pid in p_ids:
            if pid not in person_ids:
                errors.append(f"В документе {doc_id} персона {pid} отсутствует в persons!")
                
    is_valid = (len(errors) == 0)
    return is_valid, errors


def get_stats() -> Dict[str, Any]:
    """Возвращает общую сводную статистику по родословной"""
    persons = load_persons()
    families = load_families()
    sources_data = load_sources()
    documents = sources_data.get("documents", [])
    evidence = load_evidence()
    
    males = sum(1 for p in persons if p.get("sex") == "M")
    females = sum(1 for p in persons if p.get("sex") == "F")
    
    return {
        "total_persons": len(persons),
        "males": males,
        "females": females,
        "total_families": len(families),
        "total_documents": len(documents),
        "total_evidence_records": len(evidence)
    }


if __name__ == "__main__":
    valid, errs = validate_integrity()
    stats = get_stats()
    print("=== ПРОВЕРКА ЦЕЛОСТНОСТИ БАЗЫ ДАННЫХ ===")
    if valid:
        print(" Все 100% ссылок и связей проверены. Ошибок нет.")
    else:
        print(f" Найдено {len(errs)} ошибок:")
        for e in errs:
            print("  -", e)
    print("\n=== СТАТИСТИКА РОДОСЛОВНОЙ ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")
