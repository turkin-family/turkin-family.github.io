#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
serve.py - Локальный веб-сервер для интерактивного просмотра генеалогического древа.

Запуск:
    python3 serve.py
    python3 serve.py --port 8080
    python3 serve.py --no-browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import argparse
import socket

class GenealogyRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Пользовательский обработчик с корректными MIME-типами и UTF-8 заголовками"""
    
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.ged': 'text/plain; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.html': 'text/html; charset=utf-8',
        '.htm': 'text/html; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.pdf': 'application/pdf',
        '.md': 'text/markdown; charset=utf-8',
        '.txt': 'text/plain; charset=utf-8',
    }

    def end_headers(self):
        # Отключаем агрессивный кэш для комфортной локальной разработки
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def find_available_port(start_port=8080, max_attempts=20):
    port = start_port
    while is_port_in_use(port) and port < start_port + max_attempts:
        port += 1
    return port

def main():
    parser = argparse.ArgumentParser(description="Локальный сервер генеалогического проекта «Туркины»")
    parser.add_argument('--port', type=int, default=8080, help="Порт для запуска (по умолчанию: 8080)")
    parser.add_argument('--no-browser', action='store_true', help="Не открывать браузер автоматически")
    parser.add_argument('--dir', type=str, default='.', help="Корневая директория сайта (по умолчанию текущая)")
    args = parser.parse_args()

    os.chdir(args.dir)

    target_port = args.port
    if is_port_in_use(target_port):
        alt_port = find_available_port(target_port + 1)
        print(f"⚠️  Порт {target_port} занят. Переключаемся на свободный порт {alt_port}.")
        target_port = alt_port

    url = f"http://localhost:{target_port}/"

    print("=" * 65)
    print("   ЛОКАЛЬНЫЙ ВЕБ-СЕРВЕР ГЕНЕАЛОГИЧЕСКОГО ДРЕВА «ТУРКИНЫ»")
    print("=" * 65)
    print(f"  • Корневая папка:  {os.path.abspath(args.dir)}")
    print(f"  • Главная страница: {url}")
    print(f"  • Версия GEDCOM:    {url}rodoslovnaya_turkin.ged")
    print(f"  • Архив документов: {url}#archive")
    print("-" * 65)
    print("  Для завершения работы нажмите Ctrl + C")
    print("=" * 65)

    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", target_port), GenealogyRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен пользователем.")
            httpd.server_close()

if __name__ == "__main__":
    main()
