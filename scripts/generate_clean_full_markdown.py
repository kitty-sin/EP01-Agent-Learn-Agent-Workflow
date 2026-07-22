import json
import os
import glob

# Find all_sensebar_videos_with_dates.json dynamically
json_path = None
for root, dirs, files in os.walk('.'):
    if 'all_sensebar_videos_with_dates.json' in files:
        json_path = os.path.join(root, 'all_sensebar_videos_with_dates.json')
        break

if not json_path:
    # fallback search in current working directory ancestors
    candidates = glob.glob('**/all_sensebar_videos_with_dates.json', recursive=True)
    if candidates:
        json_path = candidates[0]

print("Found json_path:", json_path)

with open(json_path, 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total videos in dataset: {len(videos)}")

# Rule 5: Keep only 2025 and 2026 videos (upload_date >= 20250101)
videos_2025_plus = []
for v in videos:
    d = v.get('upload_date')
    if d and d >= '20250101':
        videos_2025_plus.append(v)

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

# Define distinct, un-nested category buckets
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

dir_path = os.path.dirname(json_path)
full_version_md_path = os.path.join(dir_path, 'Sensebar_AI_Agent_Videos_Full_Version.md')
urls_txt_path = os.path.join(dir_path, 'sensebar_urls_for_notebooklm.txt')

with open(full_version_md_path, "w", encoding="utf-8") as f:
    f.write(md_content)

with open(urls_txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(all_urls))

print("Successfully wrote updated files!")
