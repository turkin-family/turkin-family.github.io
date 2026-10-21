"""
build_genealogy.py - Экспорт родословной в стандарт GEDCOM 5.5.1
Загружает данные из реляционного хранилища data/ через data_manager.
"""

import data_manager

persons = data_manager.load_persons()
families = data_manager.load_families()

def export_gedcom(filename="rodoslovnaya_turkin.ged"):
    """Экспорт генеалогических данных в международный формат GEDCOM 5.5.1"""
    lines = [
        "0 HEAD",
        "1 SOUR AntigravityGenealogy",
        "2 VERS 1.0",
        "1 DEST ANY",
        "1 DATE 19 OCT 2026",
        "1 CHAR UTF-8",
        "1 GEDC",
        "2 VERS 5.5.1",
        "2 FORM LINEAGE-LINKED"
    ]
    
    famc_map = {}
    fams_map = {}
    for f in families:
        fid = f['id']
        husb = f.get('husb')
        wife = f.get('wife')
        if husb:
            fams_map.setdefault(husb, []).append(fid)
        if wife:
            fams_map.setdefault(wife, []).append(fid)
        for c in f.get('children', []):
            famc_map[c] = fid

    for p in persons:
        pid = p['id']
        lines.append(f"0 @{pid}@ INDI")
        lines.append(f"1 NAME {p['name']}")
        if p.get('givn'):
            lines.append(f"2 GIVN {p['givn']}")
        if p.get('surn'):
            lines.append(f"2 SURN {p['surn']}")
        lines.append(f"1 SEX {p['sex']}")
        if p.get('birt_date') or p.get('birt_plac'):
            lines.append("1 BIRT")
            if p.get('birt_date'):
                lines.append(f"2 DATE {p['birt_date']}")
            if p.get('birt_plac'):
                lines.append(f"2 PLAC {p['birt_plac']}")
        if p.get('deat_date') or p.get('deat_plac'):
            lines.append("1 DEAT")
            if p.get('deat_date'):
                lines.append(f"2 DATE {p['deat_date']}")
            if p.get('deat_plac'):
                lines.append(f"2 PLAC {p['deat_plac']}")
        if pid in famc_map:
            lines.append(f"1 FAMC @{famc_map[pid]}@")
        if pid in fams_map:
            for fid in fams_map[pid]:
                lines.append(f"1 FAMS @{fid}@")
        for n in p.get('notes', []):
            lines.append(f"1 NOTE {n}")

    for f in families:
        fid = f['id']
        lines.append(f"0 @{fid}@ FAM")
        if f.get('husb'):
            lines.append(f"1 HUSB @{f['husb']}@")
        if f.get('wife'):
            lines.append(f"1 WIFE @{f['wife']}@")
        if f.get('marr_date'):
            lines.append("1 MARR")
            lines.append(f"2 DATE {f['marr_date']}")
        for c in f.get('children', []):
            lines.append(f"1 CHIL @{c}@")
        if f.get('note'):
            lines.append(f"1 NOTE {f['note']}")

    lines.append("0 TRLR")
    content = "\n".join(lines) + "\n"
    with open(filename, "w", encoding="utf-8") as out:
        out.write(content)
    print(f"Exported GEDCOM with {len(persons)} persons and {len(families)} families to {filename}")

if __name__ == "__main__":
    export_gedcom()
