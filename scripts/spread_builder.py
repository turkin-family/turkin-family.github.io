#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/spread_builder.py - Генератор эталонных двухстраничных разворотов архивных дел.

Создает изображение полного разворота архивного тома (2200 x 1960 px):
  - Левая половина: Мужеский пол (л. об.)
  - Центр: gap (разделитель 20 px с тенью переплета)
  - Правая половина: Женский пол (л.)
  - Поля и отступы подложки
  - Автоматическая генерация оптимизированного превью (превью/*.jpg)

Пример использования:
    python3 scripts/spread_builder.py \
        --left архив_сканы_первоисточников/1816_crops/kokvitsy_l352ob_male.jpg \
        --right архив_сканы_первоисточников/1816_crops/kokvitsy_l353_female.jpg \
        --output архив_сканы_первоисточников/1816_crops/my_spread.jpg \
        --thumb превью/my_thumb.jpg
"""

import sys
import os
import argparse
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

CANVAS_WIDTH = 2200
CANVAS_HEIGHT = 1960
PAGE_MAX_WIDTH = 1080
PAGE_MAX_HEIGHT = 1900
GAP_WIDTH = 20
BG_COLOR = (241, 241, 241)  # Античный архивный пергамент

def create_spread(left_path: str, right_path: str, output_path: str, thumb_path: str = None) -> bool:
    """Смонтировать полный двухстраничный разворот с книжным переплетом."""
    if not os.path.exists(left_path):
        print(f"❌ Ошибка: Левый файл не найден: {left_path}")
        return False
    if not os.path.exists(right_path):
        print(f"❌ Ошибка: Правый файл не найден: {right_path}")
        return False

    im_left = Image.open(left_path).convert("RGB")
    im_right = Image.open(right_path).convert("RGB")

    # Создаем основной холст
    canvas = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), BG_COLOR)

    # Пропорциональное масштабирование страниц под максимальные размеры
    def fit_page(im):
        w, h = im.size
        scale = min(PAGE_MAX_WIDTH / w, PAGE_MAX_HEIGHT / h, 1.0)
        new_w, new_h = int(w * scale), int(h * scale)
        if (new_w, new_h) != (w, h):
            return im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return im

    p_left = fit_page(im_left)
    p_right = fit_page(im_right)

    # Вычисляем координаты размещения
    # Левая страница примыкает к центральному разделителю
    mid_x = CANVAS_WIDTH // 2  # 1100
    left_x = mid_x - (GAP_WIDTH // 2) - p_left.size[0]
    left_y = (CANVAS_HEIGHT - p_left.size[1]) // 2

    right_x = mid_x + (GAP_WIDTH // 2)
    right_y = (CANVAS_HEIGHT - p_right.size[1]) // 2

    # Вставка страниц
    canvas.paste(p_left, (left_x, left_y))
    canvas.paste(p_right, (right_x, right_y))

    # Наложение тени переплета (книжный корешок в зоне gap)
    spine_overlay = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(spine_overlay)

    # Рисуем тень переплета
    spine_x1 = mid_x - 12
    spine_x2 = mid_x + 12
    draw.rectangle([spine_x1, 0, spine_x2, CANVAS_HEIGHT], fill=(0, 0, 0, 45))
    draw.rectangle([mid_x - 4, 0, mid_x + 4, CANVAS_HEIGHT], fill=(0, 0, 0, 65))

    # Размываем тень
    spine_overlay = spine_overlay.filter(ImageFilter.GaussianBlur(radius=4))
    canvas.paste(spine_overlay, (0, 0), spine_overlay)

    # Сохраняем разворот
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    canvas.save(output_path, "JPEG", quality=92, optimize=True)
    print(f"✅ Создан полный 2-страничный разворот: {output_path} ({canvas.size[0]}x{canvas.size[1]})")

    # Генерация превью
    if thumb_path:
        os.makedirs(os.path.dirname(os.path.abspath(thumb_path)), exist_ok=True)
        thumb = canvas.copy()
        thumb.thumbnail((440, 392), Image.Resampling.LANCZOS)
        thumb.save(thumb_path, "JPEG", quality=85, optimize=True)
        print(f"✅ Создано превью разворота: {thumb_path}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Сборщик 2-страничных архивных разворотов")
    parser.add_argument("--left", required=True, help="Путь к скану левой страницы (л. об. — Мужской пол)")
    parser.add_argument("--right", required=True, help="Путь к скану правой страницы (л. — Женский пол)")
    parser.add_argument("--output", required=True, help="Путь для сохранения разворота .jpg")
    parser.add_argument("--thumb", default=None, help="Путь для сохранения миниатюры .jpg")
    args = parser.parse_args()

    success = create_spread(args.left, args.right, args.output, args.thumb)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
