import json

with open('all_sensebar_videos_with_dates.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total videos loaded: {len(videos)}")

# Rule 5: Filter for 2025 and 2026 only (upload_date >= '20250101')
videos_2025_plus = []
for v in videos:
    d = v.get('upload_date')
    if d and d >= '20250101':
        videos_2025_plus.append(v)

print(f"Videos published in 2025 and later: {len(videos_2025_plus)}")

# Rule 1: Deduplicate by video ID
seen_ids = set()
unique_videos = []
for v in videos_2025_plus:
    if v['id'] not in seen_ids:
        seen_ids.add(v['id'])
        unique_videos.append(v)

# Rule 3: EXCLUDE ALL FELO VIDEOS
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

# Rule 2 & 4: Granular Categorization
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
    "🛠️ AI 工具與基本功系列": [],
    "🎓 AI 教學與自動化應用系列": []
}

for v in filtered_videos:
    title = v['title']
    title_lower = title.lower()

    # Rule 2: Strict separation between Claude Code and GPT Codex
    if "antigravity" in title_lower or "anti gravity" in title_lower:
        cat = "🌌 Google AntiGravity 系列"
    elif "opencode" in title_lower:
        cat = "🔓 OpenCode 開源 Agent 系列"
    elif "codex" in title_lower or "gptcodex" in title_lower or "gpt-codex" in title_lower or "codex" in title_lower:
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
    elif "基本功" in title_lower or "工具" in title_lower or "obsidian" in title_lower or "firebase" in title_lower or "supabase" in title_lower:
        cat = "🛠️ AI 工具與基本功系列"
    elif any(k in title_lower for k in ["ai", "教學", "備課", "自動化", "批改", "考卷", "聲音", "語音"]):
        cat = "🎓 AI 教學與自動化應用系列"
    else:
        continue # Skip general non-AI videos if any

    categories[cat].append(v)

total_categorized = sum(len(lst) for lst in categories.values())
print(f"\nTotal categorized 2025+ videos: {total_categorized}")

print("\n--- Breakdown by Category ---")
for cat, lst in categories.items():
    print(f"{cat}: {len(lst)} 部")
