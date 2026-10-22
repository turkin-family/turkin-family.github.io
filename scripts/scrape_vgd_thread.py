#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_vgd_thread.py - Скачивание и структурирование всех страниц треда ВГД № 44698
«Яренский уезд Вологодской губернии - история, демография, миграционные процессы».

Сохраняет:
  - Сырые HTML-страницы в docs/raw_sources/vgd_yarensk_thread/
  - Единый структурированный JSON со всеми сообщениями в docs/raw_sources/vgd_thread_44698.json
"""

import os
import sys
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup

RAW_DIR = "docs/raw_sources/vgd_yarensk_thread"
JSON_OUTPUT = "docs/raw_sources/vgd_thread_44698.json"
BASE_URL = "https://forum.vgd.ru/3539/44698/{offset}.htm?a=stdforum_view&o="
TOTAL_OFFSETS = list(range(0, 1660, 10)) # 166 pages (0 .. 1650)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
}

def download_page(offset):
    page_num = (offset // 10) + 1
    file_path = os.path.join(RAW_DIR, f"page_{page_num:03d}_offset_{offset}.html")
    
    if os.path.exists(file_path) and os.path.getsize(file_path) > 1000:
        return page_num, offset, True, "cached"
        
    url = BASE_URL.format(offset=offset)
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200 and len(r.content) > 1000:
                with open(file_path, "wb") as f:
                    f.write(r.content)
                time.sleep(0.15)
                return page_num, offset, True, "downloaded"
            time.sleep(1.0)
        except Exception as e:
            time.sleep(1.5)
            
    return page_num, offset, False, "failed"

def parse_page(file_path, page_num, offset):
    with open(file_path, "rb") as f:
        html = f.read().decode('cp1251', errors='replace')
        
    soup = BeautifulSoup(html, 'html.parser')
    posts_data = []
    
    tables = soup.find_all('table', class_=lambda c: c and 'posttable' in c)
    for i, post in enumerate(tables):
        prev_a = post.find_previous('a', attrs={'name': re.compile(r'^pp\d+')})
        post_id = prev_a['name'].replace('pp', '') if prev_a else f"{page_num}_{i+1}"
        
        author_elem = post.find('a', class_='username')
        author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
        
        tds = post.find_all('td')
        text = ""
        date_str = ""
        
        if len(tds) > 1:
            full_text = tds[1].get_text(separator="\n", strip=True)
            # Find date in header lines
            lines = [l.strip() for l in full_text.split('\n') if l.strip()]
            date_matches = [l for l in lines[:6] if re.search(r'\b(19\d\d|20\d\d)\b', l)]
            if date_matches:
                date_str = date_matches[0]
            text = full_text
            
        posts_data.append({
            'page': page_num,
            'offset': offset,
            'post_id': post_id,
            'author': author,
            'date': date_str,
            'link': f"https://forum.vgd.ru/index.php?t=44698&p={post_id}#pp{post_id}",
            'text': text
        })
        
    return posts_data

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"=== Скачивание 166 страниц треда ВГД № 44698 в {RAW_DIR} ===")
    
    total = len(TOTAL_OFFSETS)
    done = 0
    cached = 0
    downloaded = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(download_page, off): off for off in TOTAL_OFFSETS}
        for future in as_completed(futures):
            page_num, offset, success, status = future.result()
            done += 1
            if status == "cached":
                cached += 1
            elif status == "downloaded":
                downloaded += 1
            else:
                failed += 1
            if done % 20 == 0 or done == total:
                print(f"[{done}/{total}] Скачано: {downloaded}, Из кэша: {cached}, Ошибок: {failed}")
                
    print(f"\nВсе страницы получены (всего: {done}, скачано новых: {downloaded}, кэш: {cached}, сбоев: {failed}).")
    
    # Парсинг в единый JSON
    print("\n=== Извлечение и структурирование сообщений ===")
    all_posts = []
    raw_files = sorted([f for f in os.listdir(RAW_DIR) if f.startswith("page_") and f.endswith(".html")])
    for f in raw_files:
        m = re.match(r'page_(\d+)_offset_(\d+)\.html', f)
        if m:
            p_num = int(m.group(1))
            off = int(m.group(2))
            f_path = os.path.join(RAW_DIR, f)
            p_posts = parse_page(f_path, p_num, off)
            all_posts.extend(p_posts)
            
    with open(JSON_OUTPUT, "w", encoding="utf-8") as out_f:
        json.dump(all_posts, out_f, ensure_ascii=False, indent=2)
        
    print(f"Сохранено {len(all_posts)} сообщений в {JSON_OUTPUT} (размер: {os.path.getsize(JSON_OUTPUT) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
