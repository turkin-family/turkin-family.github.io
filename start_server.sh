#!/usr/bin/env bash
# start_server.sh - Быстрый запуск локального веб-сервера
cd "$(dirname "$0")" || exit 1
python3 serve.py "$@"
