"""
archive_catalog.py - Каталог архивных первоисточников родословной Туркиных.
Загружает структурированные документы из data/sources.json через data_manager.
"""

import data_manager

_sources_data = data_manager.load_sources()

DOCS_CATALOG = _sources_data.get("documents", [])
PDF_ALBUMS = _sources_data.get("pdf_albums", [])

if __name__ == "__main__":
    print(f"Каталог архивов загружен: {len(DOCS_CATALOG)} документов, {len(PDF_ALBUMS)} PDF-альбомов.")
