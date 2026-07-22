import json
import subprocess
import os

# Write a self-contained script that fetches and outputs the markdown cleanly
cmd = [
    'python', '-m', 'yt_dlp',
    '--print', '%(id)s\t%(upload_date)s\t%(title)s',
    '--no-check-certificates',
    'https://www.youtube.com/@sensebar/videos',
    'https://www.youtube.com/@sensebar/streams',
    'https://www.youtube.com/@sensebar/shorts'
]

print("Fetching metadata with dates...")
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

video_dict = {}
for raw_line in proc.stdout:
    line = raw_line.decode('utf-8', errors='replace').strip()
    if line:
        parts = line.split('\t')
        if len(parts) >= 3:
            v_id, d, title = parts[0], parts[1], parts[2]
            if v_id not in video_dict:
                video_dict[v_id] = {
                    'id': v_id,
                    'upload_date': d,
                    'title': title,
                    'url': f'https://www.youtube.com/watch?v={v_id}'
                }

proc.wait()
videos = list(video_dict.values())
print(f"Total fetched videos: {len(videos)}")

# Rule 5: Keep only 2025 and 2026 videos (upload_date >= 20250101)
videos_2025_plus = [v for v in videos if v.get('upload_date') and v.get('upload_date') >= '20250101']
print(f"Total videos published in 2025 and 2026: {len(videos_2025_plus)}")

# Rule 1: Strict Deduplication by ID and normalized Title
seen_ids = set()
seen_titles = set()
unique_videos = []

for v in videos_2025_plus:
    v_id = v['id']
    title = v['title'].strip()
    norm_title = title.lower().replace(" ", "").replace("_", "").replace(":", "")
    
    if v_id in seen_ids or norm_title in seen_titles:
        continue
    
    seen_ids.add(v_id)
    seen_titles.add(norm_title)
    unique_videos.append(v)

print(f"Unique 2025+ videos after deduplication: {len(unique_videos)}")

# Rule 3: Exclude ALL Felo videos
filtered_videos = []
felo_count = 0
for v in unique_videos:
    title_lower = v['title'].lower()
    if 'felo' in title_lower:
        felo_count += 1
        continue
    filtered_videos.append(v)

print(f"Excluded Felo videos: {felo_count}")
print(f"Remaining valid 2025+ videos: {len(filtered_videos)}")

# Rule 2 & 4: Granular Category Buckets
category_map = {
    "🤖 AI Agent 核心觀念、架構與實戰系列": [],
    "🌌 Google AntiGravity 系列": [],
    "⚡ Claude AI & Claude Code 系列": [],
    "🛠️ GPT Codex 系列": [],
    "🔓 OpenCode 開源 Agent 系列": [],
    "📖 NotebookLM 專題系列": [],
    "📊 AI 簡報與視覺化工具系列": [],
    "🌐 Google AI / Gemini / Canvas 系列": [],
    "💬 ChatGPT & OpenAI 專題系列": [],
    "🛠️ AI 工具 & 基本功系列": [],
    "🎓 AI 教學與自動化應用系列": []
}

ai_keywords = [
    'ai', 'agent', 'claude', 'codex', 'antigravity', 'opencode', 'chatgpt', 'gpt',
    'gemini', 'notebooklm', 'notebook', '簡報', '基本功', '應用', '工具', '程式',
    'mcp', 'obsidian', 'supabase', 'firebase', 'github', 'gas', 'vibe', '繪圖',
    '生圖', '語音', '自動化', '備課', '思考模型', '大模型', '開源', 'bot', '提示詞',
    'prompt', 'dall-e', 'midjourney', 'sora', 'deepseek', 'kimi', 'glm', '導師助理',
    '助教', '一桌三櫃', '二號大腦', '第二大腦'
]

for v in filtered_videos:
    title = v['title']
    title_lower = title.lower()

    if not any(kw in title_lower for kw in ai_keywords):
        continue

    # Strict separation & priority mapping
    if "antigravity" in title_lower or "anti gravity" in title_lower:
        cat = "🌌 Google AntiGravity 系列"
    elif "opencode" in title_lower:
        cat = "🔓 OpenCode 開源 Agent 系列"
    elif "codex" in title_lower or "gptcodex" in title_lower or "gpt-codex" in title_lower:
        cat = "🛠️ GPT Codex 系列"
    elif "claude" in title_lower:
        cat = "⚡ Claude AI & Claude Code 系列"
    elif "notebooklm" in title_lower or "notebook lm" in title_lower:
        cat = "📖 NotebookLM 專題系列"
    elif "簡報" in title_lower or "padlet" in title_lower or "slides" in title_lower:
        cat = "📊 AI 簡報與視覺化工具系列"
    elif "agent" in title_lower or "mcp" in title_lower or "代理" in title_lower or "subagent" in title_lower:
        cat = "🤖 AI Agent 核心觀念、架構與實戰系列"
    elif "gemini" in title_lower or "google ai" in title_lower or "canvas" in title_lower or "google classroom" in title_lower or "gas" in title_lower:
        cat = "🌐 Google AI / Gemini / Canvas 系列"
    elif "chatgpt" in title_lower or "openai" in title_lower or "gpt-4" in title_lower or "gpt" in title_lower:
        cat = "💬 ChatGPT & OpenAI 專題系列"
    elif "基本功" in title_lower or "obsidian" in title_lower or "firebase" in title_lower or "supabase" in title_lower or "github" in title_lower:
        cat = "🛠️ AI 工具 & 基本功系列"
    else:
        cat = "🎓 AI 教學與自動化應用系列"

    category_map[cat].append(v)

total_categorized = sum(len(lst) for lst in category_map.values())
print(f"Total strictly categorized 2025+ videos: {total_categorized}")

md_lines = []
md_lines.append("# 📺 SenseBar (@sensebar) AI / Agent / Claude / Codex / AntiGravity / OpenCode 完整影片清單 (2025-2026 精選版)")
md_lines.append("")
md_lines.append("> **頻道網址**：https://www.youtube.com/@sensebar  ")
md_lines.append("> **整理日期**：2026-07-22  ")
md_lines.append(f"> **篩選標準**：發布日期為 **2025 年及以後 (2025-01-01 至 2026 年)** 之影片，全數**嚴謹去重**、**徹底排除 Felo**，並將 **Claude AI/Code**, **GPT Codex**, **NotebookLM**, **AI 簡報**, **ChatGPT/OpenAI**, **AI 工具與基本功** 等專題嚴格拆分為獨立主題分類。每部影片網址均**獨立換行**呈現。")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

all_urls = []

for cat_name, v_list in category_map.items():
    if not v_list:
        continue
    v_list_sorted = sorted(v_list, key=lambda x: x.get('upload_date', ''), reverse=True)
    
    md_lines.append(f"## {cat_name} (共 {len(v_list_sorted)} 部)")
    md_lines.append("")
    for idx, item in enumerate(v_list_sorted, 1):
        formatted_date = f"{item['upload_date'][:4]}-{item['upload_date'][4:6]}-{item['upload_date'][6:]}" if item.get('upload_date') else "2025"
        md_lines.append(f"{idx}. [{formatted_date}] {item['title']}")
        md_lines.append(item['url'])
        md_lines.append("")
        all_urls.append(item['url'])
    md_lines.append("---")
    md_lines.append("")

md_content = "\n".join(md_lines)

with open("Sensebar_AI_Agent_Videos_Full_Version.md", "w", encoding="utf-8") as f:
    f.write(md_content)

with open("sensebar_urls_for_notebooklm.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_urls))

print("ALL DONE! Successfully generated Sensebar_AI_Agent_Videos_Full_Version.md and sensebar_urls_for_notebooklm.txt")
