import os
import re
import glob

workspace = os.getcwd()
md_path = os.path.join(workspace, 'Sensebar_AI_Agent_Videos_Full_Version.md')
subtitles_dir = os.path.join(workspace, 'subtitles')

# Parse Markdown file to get correct titles and categories
print("Parsing video list from markdown...")
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

videos = []
current_category = "未知分類"

for i, line in enumerate(lines):
    line_s = line.strip()
    if not line_s:
        continue
    
    if line_s.startswith("## "):
        current_category = line_s.replace("## ", "").strip()
        current_category = re.sub(r'\(共 \d+ 部\)', '', current_category).strip()
        continue
    
    m_item = re.match(r'^\d+\.\s+(.*)$', line_s)
    if m_item:
        title = m_item.group(1).strip()
        url = None
        for j in range(i + 1, min(i + 5, len(lines))):
            next_line = lines[j].strip()
            if next_line.startswith("http"):
                url = next_line
                break
        
        if url:
            m_id = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})', url)
            v_id = m_id.group(1) if m_id else None
            if v_id:
                videos.append({
                    'category': current_category,
                    'title': title,
                    'id': v_id
                })

print(f"Total videos parsed: {len(videos)}")

def sanitize_filename(name):
    # Remove Windows invalid path characters
    clean = re.sub(r'[\\/*?:"<>|]', '', name)
    # Remove emojis (anything above 0x1f000)
    clean = "".join(c for c in clean if ord(c) < 0x1f000)
    # Strip standard symbols if they appear at the start
    clean = re.sub(r'^[\s⚡⭐✨🤖🌌📊🌐💬🔓⚡🎓🛠️📖🤖]+', '', clean)
    return clean.strip()

# Scan subtitles folder and rename files
print("Renaming subtitle files...")
renamed_count = 0
not_found_count = 0

for v in videos:
    clean_cat = sanitize_filename(v['category'])
    clean_title = sanitize_filename(v['title'])
    
    # Standard clean name: Category - Title (ID).md
    new_filename = f"{clean_cat} - {clean_title} ({v['id']}).md"
    new_path = os.path.join(subtitles_dir, new_filename)
    
    # Find existing file by ID suffix e.g. "*({id}).md"
    search_pattern = os.path.join(subtitles_dir, f"*({v['id']}).md")
    matching_files = glob.glob(search_pattern)
    
    if matching_files:
        old_path = matching_files[0]
        old_filename = os.path.basename(old_path)
        
        if old_path != new_path:
            try:
                # If target already exists, remove it first
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {old_filename}: {e}")
        else:
            # Already has correct name
            pass
    else:
        print(f"No file found for ID {v['id']}")
        not_found_count += 1

print("\n--- Renaming Completed ---")
print(f"Renamed: {renamed_count}")
print(f"Missing files: {not_found_count}")
