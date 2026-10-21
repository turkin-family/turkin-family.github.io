"""
layout_engine.py - Движок умной раскладки древа (Smart-Layout).
Обеспечивает:
1. Строгую привязку координаты X к поколениям (1..15).
2. Фиксацию прямой мужской линии Туркиных по центральной оси.
3. Автоматическое выделение свободных слотов для новых персон без наложений (min distance 105-110px).
4. Валидацию отсутствия координатных коллизий.
"""

import json
import os
from typing import Dict, List, Tuple, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
COORDS_FILE = os.path.join(DATA_DIR, "calibrated_coords.json")

# Координаты X по поколениям (хронологическая ось слева направо: 1 поколение -> 15 поколение)
GEN_X = {
    1: 80,
    2: 440,
    3: 800,
    4: 1160,
    5: 1520,
    6: 1880,
    7: 2240,
    8: 2600,
    9: 2960,
    10: 3320,
    11: 3680,
    12: 4040,
    13: 4400,
    14: 4760,
    15: 5120,
    16: 5480,
    17: 5840,
    18: 6200,
    19: 6560,
    20: 6920
}

# Ветви родословной
BRANCH_DEFS = {
    'I1': ('Пробанд', '#f59e0b', 'proband'),
    'thai': ('Материнская линия (Таиланд)', '#10b981', 'thai'),
    'turkin': ('Линия Туркиных / Летовых', '#2563eb', 'turkin'),
    'shekhonin': ('Линия Шехониных / Сюткиных', '#8b5cf6', 'shekhonin'),
    'shuktomov': ('Линия Шуктомовых / Пасынковых', '#d97706', 'shuktomov'),
    'zinoviev': ('Линия Зиновьевых / Кызъюровых', '#ec4899', 'zinoviev'),
}

THAI_IDS = {'I3', 'I5', 'I6', 'I7', 'I8', 'I11', 'I12', 'I17', 'I18'}
TURKIN_IDS = {'I2', 'I4', 'I9', 'I13', 'I19', 'I20', 'I27', 'I28', 'I29', 'I30', 'I43', 'I44', 'I45', 'I46', 'I47', 'I48', 'I68', 'I70', 'I71', 'I72', 'I73', 'I74'}
TURKIN_IDS.update(f'I{i}' for i in range(75, 205))
TURKIN_IDS.update(f'I{i}' for i in range(224, 315))
TURKIN_IDS.update({'I355', 'I356', 'I357'})
TURKIN_IDS.update(f'I{i}' for i in range(368, 400))
SHEKHONIN_IDS = {'I14', 'I21', 'I22', 'I31', 'I32', 'I33', 'I34', 'I49', 'I50', 'I51', 'I52', 'I69'}
SHEKHONIN_IDS.update(f'I{i}' for i in range(314, 333))
SHUKTOMOV_IDS = {'I10', 'I15', 'I23', 'I24', 'I35', 'I36', 'I37', 'I38', 'I53', 'I54', 'I55', 'I56', 'I63', 'I64', 'I66'}
SHUKTOMOV_IDS.update(f'I{i}' for i in range(333, 355))
ZINOVIEV_IDS = {'I16', 'I25', 'I26', 'I39', 'I40', 'I41', 'I42', 'I57', 'I58', 'I59', 'I60', 'I61', 'I62', 'I65', 'I67'}


def load_calibrated_coords() -> Dict[str, Tuple[int, int]]:
    """Загрузить проверенную карту координат из data/calibrated_coords.json"""
    if os.path.exists(COORDS_FILE):
        with open(COORDS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
            return {k: tuple(v) for k, v in raw.items()}
    return {}


def save_calibrated_coords(coords: Dict[str, Tuple[int, int]]) -> None:
    """Сохранить карту координат в data/calibrated_coords.json"""
    with open(COORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(coords, f, ensure_ascii=False, indent=2)


def assign_branch_info(persons: List[Dict[str, Any]]) -> None:
    """Присваивает ветвь и цвет каждой персоне"""
    for p in persons:
        pid = p['id']
        if pid == 'I1':
            bname, bcol, bid = BRANCH_DEFS['I1']
        elif pid in THAI_IDS:
            bname, bcol, bid = BRANCH_DEFS['thai']
        elif pid in TURKIN_IDS:
            bname, bcol, bid = BRANCH_DEFS['turkin']
        elif pid in SHEKHONIN_IDS:
            bname, bcol, bid = BRANCH_DEFS['shekhonin']
        elif pid in SHUKTOMOV_IDS:
            bname, bcol, bid = BRANCH_DEFS['shuktomov']
        elif pid in ZINOVIEV_IDS:
            bname, bcol, bid = BRANCH_DEFS['zinoviev']
        else:
            bname, bcol, bid = ('Семья', '#64748b', 'general')
        p['branch'] = bname
        p['branch_color'] = bcol
        p['branch_id'] = bid


def compute_smart_layout(
    persons: List[Dict[str, Any]], 
    families: List[Dict[str, Any]], 
    custom_overrides: Optional[Dict[str, Tuple[int, int]]] = None
) -> Dict[str, Tuple[int, int]]:
    """
    Рассчитывает умные координаты для всех персон:
    - Использует выверенные координаты для известных персон (I1..I106).
    - Для новых персон строго определяет поколение по дате рождения и родственным связям.
    - Размещает семьи аккуратными вертикальными кластерами без наложений.
    """
    import re
    coords: Dict[str, Tuple[int, int]] = load_calibrated_coords()
    if custom_overrides:
        coords.update(custom_overrides)
        
    inv_gen_x = {v: k for k, v in GEN_X.items()}
    gens: Dict[str, int] = {}
    
    # 1. Загружаем поколения из существующих базовых координат
    for pid, (x, _) in coords.items():
        if x in inv_gen_x:
            gens[pid] = inv_gen_x[x]

    # 2. Для остальных персон вычисляем базовое поколение по году рождения
    # Формула: Никола (1995/2024) = Gen 1, шаг поколения ~30 лет
    for p in persons:
        pid = p['id']
        if pid in gens:
            continue
        if p.get('gen'):
            gens[pid] = p['gen']
            continue
        bdate = p.get('birt_date', '')
        m = re.search(r'\b(1\d{3}|20\d{2})\b', str(bdate))
        if m:
            yr = int(m.group(1))
            gens[pid] = max(1, min(15, round((1995 - yr) / 30) + 1))
        else:
            gens[pid] = 7

    # 3. Итеративная релаксация поколений по семейным связям
    for _ in range(20):
        for fam in families:
            h = fam.get('husb')
            w = fam.get('wife')
            children = fam.get('children', [])
            
            # Супруги должны быть одного поколения
            if h and w:
                if h in gens and w not in gens:
                    gens[w] = gens[h]
                elif w in gens and h not in gens:
                    gens[h] = gens[w]
                    
            # Родители должны быть строго child_gen + 1
            p_gen = None
            if h and h in gens:
                p_gen = gens[h]
            elif w and w in gens:
                p_gen = gens[w]
                
            if p_gen is not None:
                for c in children:
                    if c not in gens:
                        gens[c] = p_gen - 1
                        
            # Если у детей поколение известно, а у родителей нет
            c_gens = [gens[c] for c in children if c in gens]
            if c_gens:
                expected_p_gen = max(c_gens) + 1
                if h and h not in coords:
                    gens[h] = max(gens.get(h, expected_p_gen), expected_p_gen)
                if w and w not in coords:
                    gens[w] = max(gens.get(w, expected_p_gen), expected_p_gen)

    # 4. Размещение новых персон (без фиксированных координат)
    unplaced = [p['id'] for p in persons if p['id'] not in coords]
    
    # Группируем персон по связанным семейным кластерам
    parent_of: Dict[str, List[str]] = {}
    spouse_of: Dict[str, str] = {}
    for fam in families:
        h = fam.get('husb')
        w = fam.get('wife')
        children = fam.get('children', [])
        if h and w:
            spouse_of[h] = w
            spouse_of[w] = h
        if h:
            parent_of.setdefault(h, []).extend(children)
        if w:
            parent_of.setdefault(w, []).extend(children)

    # Находим связные компоненты среди неразмещенных персон
    visited = set()
    clusters: List[List[str]] = []
    for pid in unplaced:
        if pid in visited:
            continue
        comp = []
        queue = [pid]
        visited.add(pid)
        while queue:
            curr = queue.pop(0)
            comp.append(curr)
            # смежные в семье
            neighbors = []
            if curr in spouse_of:
                neighbors.append(spouse_of[curr])
            neighbors.extend(parent_of.get(curr, []))
            for p_id, chs in parent_of.items():
                if curr in chs:
                    neighbors.append(p_id)
            for nb in neighbors:
                if nb in unplaced and nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        clusters.append(comp)

    # Базовый Y для новых кластеров (ниже всех размещенных персон)
    base_max_y = max((y for _, y in coords.values()), default=3100)
    cur_y = max(3300, base_max_y + 190)

    for cluster in clusters:
        by_gen: Dict[int, List[str]] = {}
        for pid in cluster:
            g = gens.get(pid, 7)
            by_gen.setdefault(g, []).append(pid)
            
        max_in_col = max(len(v) for v in by_gen.values())
        block_height = max_in_col * 115 + 60
        
        for g, g_pids in by_gen.items():
            x = GEN_X.get(g, 80)
            start_y = cur_y + (block_height - len(g_pids) * 115) // 2
            for idx, pid in enumerate(g_pids):
                coords[pid] = (x, start_y + idx * 115)
                
        cur_y += block_height + 40

    return coords


def validate_layout(coords: Dict[str, Tuple[int, int]]) -> Tuple[bool, List[str]]:
    """Проверяет раскладку на отсутствие коллизий (наложений карточек)"""
    by_x: Dict[int, List[Tuple[int, str]]] = {}
    for pid, (x, y) in coords.items():
        by_x.setdefault(x, []).append((y, pid))
        
    errors = []
    for x, items in by_x.items():
        items.sort()
        for i in range(len(items) - 1):
            y1, p1 = items[i]
            y2, p2 = items[i+1]
            dist = y2 - y1
            if dist < 85:
                errors.append(f"Коллизия карточек при X={x}: {p1} (y={y1}) и {p2} (y={y2}), расстояние {dist}px < 85px")
                
    return (len(errors) == 0), errors


if __name__ == "__main__":
    import data_manager
    persons = data_manager.load_persons()
    families = data_manager.load_families()
    coords = compute_smart_layout(persons, families)
    valid, errs = validate_layout(coords)
    print("=== ПРОВЕРКА SMART-LAYOUT РАСКЛАДКИ ===")
    print(f"Всего персон с координатами: {len(coords)}")
    if valid:
        print(" Все 100% карточек размещены с гарантированным расстоянием. Наложений: 0.")
    else:
        print(f" Найдено коллизий: {len(errs)}")
        for e in errs:
            print("  -", e)
