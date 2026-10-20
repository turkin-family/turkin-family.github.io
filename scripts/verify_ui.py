import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        errors = []
        page.on('console', lambda msg: errors.append(f'[{msg.type}] {msg.text}') if msg.type == 'error' else None)
        
        file_path = 'file://' + os.path.abspath('index.html')
        page.goto(file_path)
        page.wait_for_timeout(1500)
        
        print('Console errors:', len(errors))
        for e in errors:
            print('  -', e)
            
        links_info = page.evaluate('''() => {
            const svg = document.getElementById('svgLinksLayer');
            const paths = Array.from(svg.querySelectorAll('path'));
            const directPairs = [
                ['I43', 'I70'],
                ['I70', 'I148'],
                ['I148', 'I80'],
                ['I80', 'I78'],
                ['I78', 'I71'],
                ['I71', 'I72'],
                ['I72', 'I73'],
                ['I73', 'I74']
            ];
            const found = {};
            paths.forEach(p => {
                const id = p.getAttribute('id') || '';
                directPairs.forEach(pair => {
                    const key = 'link-' + pair[0] + '-' + pair[1];
                    if (id === key) {
                        found[pair[0] + '->' + pair[1]] = true;
                    }
                });
            });
            return {
                total_paths: paths.length,
                found: found
            };
        }''')
        print('Total SVG paths:', links_info['total_paths'])
        print('Direct lineage connections found:', links_info['found'])

        # Modal for I70
        page.evaluate("openModal('I70')")
        page.wait_for_timeout(500)
        modal_name = page.locator('#modalName').inner_text()
        print('Modal for I70 name:', modal_name)
        
        # Check content inside modal
        body_text = page.locator('#modalBody').inner_text()
        print('Modal body for I70:\n', body_text[:400])

        # Check Archive tab
        page.evaluate("switchTab('archive')")
        page.wait_for_timeout(500)
        archive_docs = page.evaluate('''() => {
            const items = document.querySelectorAll('.doc-card');
            return Array.from(items).map(it => ({
                title: it.querySelector('.doc-card-title') ? it.querySelector('.doc-card-title').innerText : '',
                thumb: it.querySelector('img') ? it.querySelector('img').src : ''
            }));
        }''')
        print(f'Total archive cards: {len(archive_docs)}')
        h8_found = [d for d in archive_docs if '1834' in d['title']]
        print(f'1834 archive cards found: {len(h8_found)}')
        for h in h8_found:
            print('  *', h['title'][:65], '--> thumb:', os.path.basename(h['thumb']))

        # Take screenshot of direct lineage on the tree
        page.evaluate("switchTab('tree')")
        page.wait_for_timeout(500)
        # Pan/zoom so I70, I148, I80 are visible
        page.evaluate('''() => {
            const container = document.getElementById('treeContainer');
            // Center around X=2700, Y=800
            if (typeof setPanZoom === 'function') {
                setPanZoom(-1800, -300, 0.85);
            }
        }''')
        page.wait_for_timeout(500)
        page.screenshot(path='scripts/tree_direct_line_preview.png')
        print('Screenshot saved to scripts/tree_direct_line_preview.png')

        browser.close()

if __name__ == '__main__':
    verify()
