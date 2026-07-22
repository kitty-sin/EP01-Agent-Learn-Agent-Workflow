import json

with open('all_sensebar_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total unique videos loaded: {len(videos)}")

# Priority matching logic
categories = {
    "🤖 AI Agent 核心觀念、架構與實戰系列": [],
    "🌌 Google AntiGravity 系列": [],
    "⚡ Claude AI & Claude Code 系列": [],
    "🛠️ GPT Codex 系列": [],
    "🔓 OpenCode 開源 Agent 系列": [],
    "📖 NotebookLM / Felo / AI 簡報與視覺化工具系列": [],
    "🌐 Google AI / Gemini / Google Canvas / Classroom 系列": [],
    "💬 ChatGPT / OpenAI & AI 工具與基本功應用系列": [],
    "💡 其他 AI / 基本功應用影片": []
}

ai_keywords = [
    'ai', 'agent', 'claude', 'codex', 'antigravity', 'opencode', 'chatgpt', 'gpt',
    'gemini', 'notebooklm', 'notebook', 'felo', 'canvas', '簡報', '基本功', '應用',
    '工具', '程式', 'mcp', 'obsidian', 'supabase', 'firebase', 'github', 'gas',
    'vibe', '繪圖', '生圖', '語音', '自動化', '備課', '思考模型', '大模型', '開源', 'bot',
    '提示詞', 'prompt', 'dall-e', 'midjourney', 'sora', 'deepseek', 'kimi', 'glm',
    '導師助理', '助教', '一桌三櫃', '二號大腦', '第二大腦'
]

excluded_count = 0
included_videos = []

for v in videos:
    v_id = v['id']
    title = v['title']
    title_lower = title.lower()

    # Check relevance
    is_ai = any(kw in title_lower for kw in ai_keywords)
    if not is_ai:
        excluded_count += 1
        continue

    # Priority Classification
    if "antigravity" in title_lower or "anti gravity" in title_lower:
        cat = "🌌 Google AntiGravity 系列"
    elif "opencode" in title_lower:
        cat = "🔓 OpenCode 開源 Agent 系列"
    elif "codex" in title_lower or "gptcodex" in title_lower or "gpt-codex" in title_lower:
        cat = "🛠️ GPT Codex 系列"
    elif "claude" in title_lower:
        cat = "⚡ Claude AI & Claude Code 系列"
    elif "agent" in title_lower or "mcp" in title_lower or "代理" in title_lower:
        cat = "🤖 AI Agent 核心觀念、架構與實戰系列"
    elif "notebooklm" in title_lower or "notebook lm" in title_lower or "felo" in title_lower or "簡報" in title_lower:
        cat = "📖 NotebookLM / Felo / AI 簡報與視覺化工具系列"
    elif any(k in title_lower for k in ["google ai", "gemini", "canvas", "classroom", "gas"]):
        cat = "🌐 Google AI / Gemini / Google Canvas / Classroom 系列"
    elif any(k in title_lower for k in ["chatgpt", "gpt", "ai", "基本功", "應用", "工具"]):
        cat = "💬 ChatGPT / OpenAI & AI 工具與基本功應用系列"
    else:
        cat = "💡 其他 AI / 基本功應用影片"

    categories[cat].append(v)
    included_videos.append(v)

total_included = len(included_videos)
print(f"Total AI & Agent related videos included: {total_included}")
print(f"Total excluded (non-AI general vlogs): {excluded_count}")

# Generate Markdown
md_lines = []
md_lines.append("# 📺 SenseBar (@sensebar) AI / Agent / Claude / Codex / AntiGravity / OpenCode 完整影片清單 (Full Version)")
md_lines.append("")
md_lines.append("> **頻道網址**：https://www.youtube.com/@sensebar  ")
md_lines.append("> **整理日期**：2026-07-22  ")
md_lines.append(f"> **說明**：本清單完整掃瞄 SenseBar 頻道（包含上傳影片、直播重播與 Shorts 共 496 部內容），精選篩選出全數 **{total_matched_val if 'total_matched_val' in locals() else total_included} 部** 關於 **Claude AI / Claude Code**, **GPT Codex**, **Google AntiGravity**, **OpenCode**, **AI Agent**, **ChatGPT**, **Google AI**, **NotebookLM** 以及 **AI 簡報 / AI 工具 / AI 應用 / 基本功** 之教學與實戰影片。每部影片網址均獨立換行呈現，便於閱讀與批次匯入 NotebookLM。")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

all_urls = []

for cat_name, v_list in categories.items():
    if not v_list:
        continue
    md_lines.append(f"## {cat_name} (共 {len(v_list)} 部)")
    md_lines.append("")
    for idx, item in enumerate(v_list, 1):
        md_lines.append(f"{idx}. {item['title']}")
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

print("Successfully generated Sensebar_AI_Agent_Videos_Full_Version.md!")
