import os
import sys
import re
import html
import subprocess
import time
import glob

workspace = os.getcwd()
md_path = os.path.join(workspace, 'Sensebar_AI_Agent_Videos_Full_Version.md')
subtitles_dir = os.path.join(workspace, 'subtitles')
os.makedirs(subtitles_dir, exist_ok=True)

def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        # Fallback for Windows CP950 terminal
        enc = sys.stdout.encoding or 'utf-8'
        print(msg.encode(enc, errors='replace').decode(enc))

# Parse Markdown file
safe_print("Parsing video list...")
with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

videos = []
current_category = "未知分類"

for i, line in enumerate(lines):
    line_s = line.strip()
    if not line_s:
        continue
    
    # Track category
    if line_s.startswith("## "):
        current_category = line_s.replace("## ", "").strip()
        # Remove video count from category name e.g. " (共 19 部)"
        current_category = re.sub(r'\(共 \d+ 部\)', '', current_category).strip()
        continue
    
    # Match numbered items
    m_item = re.match(r'^\d+\.\s+(.*)$', line_s)
    if m_item:
        title = m_item.group(1).strip()
        # The next non-empty line should be the URL
        url = None
        for j in range(i + 1, min(i + 5, len(lines))):
            next_line = lines[j].strip()
            if next_line.startswith("http"):
                url = next_line
                break
        
        if url:
            # Extract video ID
            m_id = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})', url)
            v_id = m_id.group(1) if m_id else None
            if v_id:
                videos.append({
                    'category': current_category,
                    'title': title,
                    'url': url,
                    'id': v_id
                })

safe_print(f"Total videos parsed: {len(videos)}")

def sanitize_filename(name):
    # Remove filesystem invalid characters and emojis to prevent Windows file path issues
    clean = re.sub(r'[\\/*?:"<>|]', '', name)
    # Remove emojis
    clean = clean.encode('ascii', 'ignore').decode('ascii')
    # If empty after removing non-ascii, fallback to a clean name
    if not clean.strip():
        clean = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', name)
    return clean.strip()

def clean_vtt(vtt_content):
    lines = vtt_content.splitlines()
    cleaned_lines = []
    last_text = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if line.startswith("NOTE"):
            continue
        # Remove simple formatting/HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        line = html.unescape(line).strip()
        if not line:
            continue
        # Remove duplicate lines
        if line == last_text:
            continue
        cleaned_lines.append(line)
        last_text = line
    
    # Cumulative addition deduplication for YouTube auto-captions
    final_sentences = []
    for line in cleaned_lines:
        if final_sentences and line.startswith(final_sentences[-1]):
            final_sentences[-1] = line
        elif final_sentences and final_sentences[-1].startswith(line):
            continue
        else:
            final_sentences.append(line)
            
    return "\n\n".join(final_sentences)

# Start download process
safe_print("Starting subtitle download process...")
success_count = 0
skipped_count = 0
failed_count = 0

for idx, v in enumerate(videos, 1):
    # Get clean category and title names without invalid path characters or emojis
    clean_cat = sanitize_filename(v['category'])
    clean_title = sanitize_filename(v['title'])
    
    # Format filename: Category - Title (ID).md
    filename = f"{clean_cat} - {clean_title} ({v['id']}).md"
    file_path = os.path.join(subtitles_dir, filename)
    
    # Check if subtitle file already exists (supports resuming)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "[無字幕資訊]" in content or len(content) > 300:
            safe_print(f"[{idx}/{len(videos)}] Skipping existing: {filename}")
            skipped_count += 1
            continue
            
    safe_print(f"[{idx}/{len(videos)}] Processing: {v['title']} ({v['id']})...")
    
    # Temporary VTT output prefix
    temp_output_prefix = os.path.join(subtitles_dir, f"temp_{v['id']}")
    
    # Run yt-dlp to download subtitles/auto-subtitles
    cmd = [
        'python', '-m', 'yt_dlp',
        '--skip-download',
        '--write-subs',
        '--write-auto-subs',
        '--sub-langs', 'zh-TW,zh-Hant,zh-Hans,zh,zh-CN,zh-HK',
        '--sub-format', 'vtt',
        '--no-check-certificates',
        '--output', temp_output_prefix,
        v['url']
    ]
    
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        # Search for any downloaded VTT files matching temp_<id>*
        vtt_pattern = os.path.join(subtitles_dir, f"temp_{v['id']}.*.vtt")
        vtt_files = glob.glob(vtt_pattern)
        
        # Prepare MD header
        md_content = f"""# {v['title']}

- **影片連結**: {v['url']}
- **影片 ID**: `{v['id']}`
- **影片分類**: {v['category']}

---

"""
        
        if vtt_files:
            # Sort to prioritize zh-Hant if multiple exist
            vtt_files.sort(key=lambda x: 0 if 'zh-Hant' in x else (1 if 'zh' in x else 2))
            chosen_vtt = vtt_files[0]
            
            with open(chosen_vtt, 'r', encoding='utf-8', errors='ignore') as f:
                raw_vtt = f.read()
                
            cleaned_text = clean_vtt(raw_vtt)
            
            if cleaned_text.strip():
                md_content += cleaned_text
                success_count += 1
            else:
                md_content += "*[無字幕文字內容]*"
                failed_count += 1
                
            # Clean up temporary vtt files
            for vf in vtt_files:
                try:
                    os.remove(vf)
                except:
                    pass
        else:
            # No subtitles found or download failed
            md_content += "*[無字幕資訊]*"
            failed_count += 1
            
        # Write markdown file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        safe_print(f"Saved: {filename}")
        
    except subprocess.TimeoutExpired:
        safe_print(f"Timeout expired for video {v['id']}")
        failed_count += 1
    except Exception as e:
        safe_print(f"Error processing video {v['id']}: {e}")
        failed_count += 1
        
    # Standard rate limit delay (1.5 seconds)
    time.sleep(1.5)

safe_print("\n--- Subtitle Download Completed ---")
safe_print(f"Successfully processed: {success_count}")
safe_print(f"Skipped (already exists): {skipped_count}")
safe_print(f"No subtitle or failed: {failed_count}")
safe_print(f"Total files in subtitles/ folder: {len(os.listdir(subtitles_dir))}")
