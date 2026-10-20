#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recapture_parishes.py

Recaptures screenshots of all 17 individual biographies and the overview page
from http://parishes.ru/pers.php?no=57 with full content width (no right-side clipping),
comfortable margins, high-DPI (2x scale) rendering, and regenerated thumbnails.
"""

import os
from playwright.sync_api import sync_playwright
from PIL import Image

ENTRIES = [
    '14118', '1035', '13958', '14988', '1116', '1126', '14254', '14654',
    '14873', '13343', '13959', '2393', '14115', '14199', '7463', '1043', '14198'
]

OUT_DIR = 'архив_сканы_первоисточников/parishes_entries'
THUMB_DIR = 'архив_сканы_первоисточников/превью'

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Viewport 1440px wide, high device scale factor for ultra crisp typography
        page = browser.new_page(viewport={'width': 1440, 'height': 8500}, device_scale_factor=2)
        print("Navigating to http://parishes.ru/pers.php?no=57 ...")
        page.goto('http://parishes.ru/pers.php?no=57')
        page.wait_for_timeout(1500)

        # Style adjustment: give section.container comfortable reading width and right padding
        # and ensure .source box is clearly distinct and never cut off.
        page.evaluate("""() => {
            const style = document.createElement('style');
            style.textContent = `
                body {
                    background: #ffffff !important;
                }
                section.container {
                    width: 950px !important;
                    max-width: 950px !important;
                    padding-right: 50px !important;
                    box-sizing: border-box !important;
                    background: #ffffff !important;
                }
                .source {
                    margin-top: 10px !important;
                    margin-bottom: 12px !important;
                    padding: 8px 12px !important;
                    background: #f1f5f9 !important;
                    border-left: 3px solid #2563eb !important;
                    border-radius: 4px !important;
                    display: block !important;
                }
                .source p {
                    margin: 0 !important;
                    font-size: 0.95em !important;
                    color: #334155 !important;
                }
            `;
            document.head.appendChild(style);
        }""")
        page.wait_for_timeout(500)

        # 1. Recapture all 17 individual entries
        for eid in ENTRIES:
            box = page.evaluate("""(eid) => {
                const div = document.querySelector('div[id="' + eid + '"]');
                if (!div) return null;
                const h3 = div.querySelector('h3');
                const source = div.querySelector('.source');
                if (!h3 || !source) return null;

                const container = document.querySelector('section.container').getBoundingClientRect();
                const r1 = h3.getBoundingClientRect();
                const r2 = source.getBoundingClientRect();

                // Compute exact bounding clip with comfortable padding
                const left = Math.max(0, container.left - 15);
                const width = Math.ceil(container.width + 30);
                const top = Math.max(0, r1.top - 15);
                const height = Math.ceil((r2.bottom - r1.top) + 30);

                return {
                    x: Math.floor(left),
                    y: Math.floor(top),
                    width: Math.floor(width),
                    height: Math.floor(height)
                };
            }""", eid)

            if not box:
                print(f"Warning: box for {eid} not found!")
                continue

            out_png = os.path.join(OUT_DIR, f"parishes_{eid}.png")
            page.screenshot(path=out_png, clip=box)

            # Create thumbnail maintaining aspect ratio
            im = Image.open(out_png)
            w, h = im.size
            # High-res thumb with width 600
            thumb_w = 600
            thumb_h = int(h * (thumb_w / float(w)))
            thumb = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            thumb_path = os.path.join(THUMB_DIR, f"thumb_parishes_{eid}.jpg")
            thumb.convert('RGB').save(thumb_path, 'JPEG', quality=90)

            print(f"Saved {out_png} ({im.size}) and {thumb_path} ({thumb.size})")

        # 2. Recapture parishes_ru_pers_57.png (Overview page of Turkins clergy)
        # Capture the header and the first section with proper width
        overview_box = page.evaluate("""() => {
            const h1 = document.querySelector('h1') || document.querySelector('h2') || document.querySelector('section.container');
            const main = document.querySelector('.main_container') || document.body;
            const rMain = main.getBoundingClientRect();
            return {
                x: Math.max(0, Math.floor(rMain.left)),
                y: 0,
                width: Math.min(1300, Math.ceil(rMain.width)),
                height: 950
            };
        }""")
        overview_png = "архив_сканы_первоисточников/parishes_ru_pers_57.png"
        page.screenshot(path=overview_png, clip=overview_box)
        im_ov = Image.open(overview_png)
        w, h = im_ov.size
        thumb_ov = im_ov.resize((600, int(h * (600.0 / w))), Image.Resampling.LANCZOS)
        thumb_ov.convert('RGB').save("архив_сканы_первоисточников/превью/thumb_parishes_ru_pers_57.jpg", 'JPEG', quality=90)
        print(f"Saved overview {overview_png} ({im_ov.size})")

        browser.close()
    print("All parishes screenshots successfully recaptured without clipping!")

if __name__ == '__main__':
    main()
