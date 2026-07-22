import re
import os

with open('Sensebar_AI_Agent_Videos_Full_Version.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse categories and items from the file
lines = text.splitlines()

header_lines = []
categories = []
current_cat = None

in_header = True

for line in lines:
    if line.startswith('## '):
        in_header = False
        if current_cat:
            categories.append(current_cat)
        current_cat = {'title': line, 'items': []}
    elif in_header:
        header_lines.append(line)
    else:
        if current_cat:
            current_cat['items'].append(line)

if current_cat:
    categories.append(current_cat)

def parse_items(cat_lines):
    # Group title lines and url lines
    items = []
    curr_title = None
    curr_url = None

    for line in cat_lines:
        line_s = line.strip()
        if not line_s or line_s == '---':
            continue
        
        m_item = re.match(r'^\d+\.\s+(.*)$', line_s)
        if m_item:
            if curr_title and curr_url:
                items.append({'title': curr_title, 'url': curr_url})
            curr_title = m_item.group(1)
            curr_url = None
        elif line_s.startswith('http'):
            curr_url = line_s

    if curr_title and curr_url:
        items.append({'title': curr_title, 'url': curr_url})
    
    return items

def get_sort_key(item):
    title = item['title']
    
    # Check for EP number e.g. "EP01", "EP02", "EP09_1"
    m_ep = re.search(r'EP(\d+)(?:_(\d+))?', title, re.IGNORECASE)
    if m_ep:
        ep_main = int(m_ep.group(1))
        ep_sub = int(m_ep.group(2)) if m_ep.group(2) else 0
        # Priority 0 for EP items (ascending order: 01, 02, 03...)
        return (0, ep_main, ep_sub, title)
    else:
        # Priority 1 for non-EP items (sorted alphabetically / by title)
        return (1, 999, 0, title)

new_md_lines = header_lines[:]
if new_md_lines and new_md_lines[-1] != '':
    new_md_lines.append('')

for cat in categories:
    cat_title = cat['title']
    raw_items = parse_items(cat['items'])
    
    # Sort items using key
    sorted_items = sorted(raw_items, key=get_sort_key)
    
    # Update category title with count
    cat_header = re.sub(r'\(共 \d+ 部\)', f'(共 {len(sorted_items)} 部)', cat_title)
    
    new_md_lines.append(cat_header)
    new_md_lines.append('')
    
    for idx, item in enumerate(sorted_items, 1):
        new_md_lines.append(f"{idx}. {item['title']}")
        new_md_lines.append(item['url'])
        new_md_lines.append('')
    
    new_md_lines.append('---')
    new_md_lines.append('')

new_text = "\n".join(new_md_lines)

paths = [
    r'c:\Users\PC\Documents\Google%20Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent',
    r'C:\Users\PC\Documents\Google Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent',
    os.getcwd()
]

for p in paths:
    try:
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, 'Sensebar_AI_Agent_Videos_Full_Version.md'), 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("Successfully re-sorted:", p)
    except Exception as e:
        print("Error re-sorting:", e)

print("SUCCESSFULLY RE-SORTED ALL CATEGORIES ASCENDING BY EP NUMBER!")
