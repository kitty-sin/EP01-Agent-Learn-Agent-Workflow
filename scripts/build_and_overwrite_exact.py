import json
import os

# Find all_sensebar_videos_with_dates.json
target_json = None
for root, dirs, files in os.walk('.'):
    for fn in files:
        if fn == 'all_sensebar_videos_with_dates.json':
            target_json = os.path.join(root, fn)
            break

if not target_json:
    target_json = r'all_sensebar_videos_with_dates.json'

print("Using dataset file:", target_json)

with open(target_json, 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Loaded total channel dataset: {len(videos)} videos")

# -------------------------------------------------------------
# RULE 5: Filter for 2025 and 2026 ONLY (upload_date >= '20250101')
# -------------------------------------------------------------
videos_2025 = [v for v in videos if v.get('upload_date') and v.get('upload_date') >= '20250101']
print(f"Step 1: Videos published in 2025-2026: {len(videos_2025)}")

# -------------------------------------------------------------
# RULE 1: Strict Deduplication by Video ID and Normalized Title
# -------------------------------------------------------------
seen_ids = set()
seen_norm_titles = set()
unique_videos = []

for v in videos_2025:
    v_id = v['id']
    raw_title = v['title'].strip()
    norm = raw_title.lower().replace(" ", "").replace("_", "").replace(":", "").replace("-", "")
    
    if v_id in seen_ids or norm in seen_norm_titles:
        continue
    
    seen_ids.add(v_id)
    seen_norm_titles.add(norm)
    unique_videos.append(v)

print(f"Step 2: Unique 2025+ videos after deduplication: {len(unique_videos)}")

# -------------------------------------------------------------
# RULE 3: Exclude ALL Felo videos
# -------------------------------------------------------------
no_felo_videos = []
felo_count = 0
for v in unique_videos:
    if 'felo' in v['title'].lower():
        felo_count += 1
        continue
    no_felo_videos.append(v)

print(f"Step 3: Excluded Felo videos: {felo_count}")
print(f"Step 4: Remaining 2025+ non-Felo videos: {len(no_felo_videos)}")

# -------------------------------------------------------------
# RULES 2 & 4: Granular, Distinct Category Mapping
# -------------------------------------------------------------
categories = {
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

for v in no_felo_videos:
    title = v['title']
    title_lower = title.lower()

    if not any(kw in title_lower for kw in ai_keywords):
        continue

    # Priority mapping according to rules:
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

    categories[cat].append(v)

total_categorized = sum(len(lst) for lst in categories.values())
print(f"Step 5: Total strictly categorized 2025+ videos: {total_categorized}")

# Build Markdown Content
md_lines = []
md_lines.append("# 📺 SenseBar (@sensebar) AI / Agent / Claude / Codex / AntiGravity / OpenCode 完整影片清單 (2025-2026 精選版)")
md_lines.append("")
md_lines.append("> **頻道網址**：https://www.youtube.com/@sensebar  ")
md_lines.append("> **整理日期**：2026-07-22  ")
md_lines.append(f"> **嚴謹篩選與分類標準**：  \n> 1. **時間限制**：僅收錄 **2025 年與 2026 年** 最新發布之影片（已剔除 2024 年及更早之舊影片）。  \n> 2. **嚴謹去重**：比對影片 ID 與標題，確保無任何重複影片。  \n> 3. **排除主題**：徹底排除 Felo 相關影片。  \n> 4. **精準獨立分類**：Claude Code/AI、GPT Codex、NotebookLM、AI 簡報、ChatGPT/OpenAI、AI 工具基本功 等主題均獨立分類，絕不混淆。  \n> 5. **網址獨立換行**：每部影片標題下方之網址均獨立換行呈現，方便直接貼入 NotebookLM。")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

all_urls = []

for cat_name, v_list in categories.items():
    if not v_list:
        continue
    # Sort newest first
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
txt_content = "\n".join(all_urls)

# Save to target files in current directory
with open("Sensebar_AI_Agent_Videos_Full_Version.md", "w", encoding="utf-8") as f:
    f.write(md_content)

with open("sensebar_urls_for_notebooklm.txt", "w", encoding="utf-8") as f:
    f.write(txt_content)

print(f"SUCCESS! Written {len(all_urls)} videos to Sensebar_AI_Agent_Videos_Full_Version.md!")
