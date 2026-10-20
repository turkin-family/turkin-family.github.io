from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://parishes.ru/pers.php?no=57')
    page.wait_for_timeout(1000)
    
    entries = [
        '14118', '1035', '13958', '14988', '1116', '1126', '14254', '14654',
        '14873', '13343', '13959', '2393', '14115', '14199', '7463', '1043', '14198'
    ]
    
    all_data = []
    for eid in entries:
        t = page.evaluate("""(eid) => {
            const div = document.querySelector('div[id="' + eid + '"]');
            if (!div) return null;
            const h3 = div.querySelector('h3');
            const source = div.querySelector('.source');
            let content = '';
            let curr = h3 ? h3.nextElementSibling : null;
            while (curr && curr !== source && !curr.id) {
                content += curr.innerText + '\\n';
                curr = curr.nextElementSibling;
            }
            return {
                id: eid,
                title: h3 ? h3.innerText.trim() : '',
                content: content.trim(),
                source: source ? source.innerText.trim() : ''
            };
        }""", eid)
        if t:
            all_data.append(t)
            
    with open('scripts/all_parishes_entries_dump.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print("Dumped", len(all_data), "entries to scripts/all_parishes_entries_dump.json")
    browser.close()
