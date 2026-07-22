import json

json_path = r"C:\Users\PC\.gemini\antigravity\brain\d1555396-20ff-4bcd-b436-84c71dfd00cd\scratch\videos.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

all_videos = data["all"]

# Topics requested by user: claude ai, codex, antigravity, opencode, AI agent
# Let's filter videos into topics or identify all matching videos

categories = {
    "Claude AI / Claude": [],
    "Codex / OpenAI Codex / Code Interpreter": [],
    "Google Antigravity": [],
    "OpenCode / Open-source Agent": [],
    "AI Agent / Agent 應用與實作": [],
    "其他 AI 開發與 Coding Agent 工具 (Cursor, Bolt, Windsurf, Dev, etc.)": []
}

keywords_strict = {
    "claude": ["claude", "sonnet", "haiku", "opus"],
    "codex": ["codex", "code interpreter", "openai codex"],
    "antigravity": ["antigravity", "google antigravity"],
    "opencode": ["opencode", "open code", "open-source agent"],
    "agent": ["agent", "智能體", "代理"],
    "other_ai": ["ai", "cursor", "windsurf", "bolt", "gpt", "gemini", "copilot", "v0", "replit"]
}

relevant_videos = []

for v in all_videos:
    title = v["title"]
    url = v["url"]
    title_lower = title.lower()
    
    is_relevant = False
    tags = []
    
    if any(k in title_lower for k in keywords_strict["claude"]):
        tags.append("Claude AI")
        categories["Claude AI / Claude"].append(v)
        is_relevant = True
        
    if any(k in title_lower for k in keywords_strict["codex"]):
        tags.append("Codex")
        categories["Codex / OpenAI Codex / Code Interpreter"].append(v)
        is_relevant = True
        
    if any(k in title_lower for k in keywords_strict["antigravity"]):
        tags.append("Antigravity")
        categories["Google Antigravity"].append(v)
        is_relevant = True
        
    if any(k in title_lower for k in keywords_strict["opencode"]):
        tags.append("OpenCode")
        categories["OpenCode / Open-source Agent"].append(v)
        is_relevant = True

    if any(k in title_lower for k in keywords_strict["agent"]):
        tags.append("AI Agent")
        categories["AI Agent / Agent 應用與實作"].append(v)
        is_relevant = True

    if not is_relevant and any(k in title_lower for k in keywords_strict["other_ai"]):
        categories["其他 AI 開發與 Coding Agent 工具 (Cursor, Bolt, Windsurf, Dev, etc.)"].append(v)

    if is_relevant:
        relevant_videos.append(v)

print(f"Total channel videos: {len(all_videos)}")
print(f"Directly relevant target videos (Claude, Codex, Antigravity, OpenCode, Agent): {len(relevant_videos)}")

print("\nBreakdown by Category:")
for cat, vlist in categories.items():
    print(f"  {cat}: {len(vlist)} videos")
    for v in vlist:
        print(f"    - [{v['title']}]({v['url']})")
