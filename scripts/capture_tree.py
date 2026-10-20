import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    file_path = 'file://' + os.path.abspath('index.html')
    page.goto(file_path)
    page.wait_for_timeout(1500)
    
    # Center directly on Y=800 and X=2800 (I43, I70, I148, I80, I78)
    page.evaluate("""() => {
        panX = -1260;
        panY = 250;
        zoom = 0.75;
        updateTransform();
    }""")
    page.wait_for_timeout(500)
    page.screenshot(path='scripts/tree_direct_line_canvas.png')
    print('Screenshot saved!')
    browser.close()
