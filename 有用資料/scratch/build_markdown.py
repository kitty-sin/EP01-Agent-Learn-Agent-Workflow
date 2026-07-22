import json
import os

json_path = r"C:\Users\PC\.gemini\antigravity\brain\d1555396-20ff-4bcd-b436-84c71dfd00cd\scratch\videos.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

all_videos = data["all"]

# Define categories and matching rules
categories = {
    "🤖 AI Agent 核心觀念與實戰系列": [],
    "🌌 Google AntiGravity 系列": [],
    "⚡ Claude AI & Claude Code 系列": [],
    "🛠️ GPT Codex 系列": [],
    "🔓 OpenCode 開源 Agent 系列": [],
    "🚀 其他 AI Coding / Agent 簡報與自動化工具": []
}

for v in all_videos:
    title = v["title"]
    url = v["url"]
    t_lower = title.lower()

    if "antigravity" in t_lower:
        categories["🌌 Google AntiGravity 系列"].append(v)
    elif "opencode" in t_lower:
        categories["🔓 OpenCode 開源 Agent 系列"].append(v)
    elif "codex" in t_lower:
        categories["🛠️ GPT Codex 系列"].append(v)
    elif "claude" in t_lower or "sonnet" in t_lower:
        categories["⚡ Claude AI & Claude Code 系列"].append(v)
    elif "agent" in t_lower or "智能體" in t_lower:
        categories["🤖 AI Agent 核心觀念與實戰系列"].append(v)
    elif any(k in t_lower for k in ["mcp", "notebooklm", "vibe coding", "code interpreter", "hyperframes", "cursor", "v0", "bolt"]):
        categories["🚀 其他 AI Coding / Agent 簡報與自動化工具"].append(v)

md_content = """# 📺 SenseBar (@sensebar) AI Agent / Claude / Codex / AntiGravity / OpenCode 影片清單

> **頻道網址**：[https://www.youtube.com/@sensebar](https://www.youtube.com/@sensebar)  
> **整理日期**：2026-07-21  
> **說明**：本清單由 AI Agent 自動檢索 SenseBar 頻道中所有關於 **Claude AI**, **Codex**, **Google AntiGravity**, **OpenCode** 與 **AI Agent** 的教學與實戰影片。

---

"""

for cat, vlist in categories.items():
    md_content += f"## {cat} (共 {len(vlist)} 部)\n\n"
    if not vlist:
        md_content += "_無相關影片_\n\n"
    else:
        for idx, v in enumerate(vlist, 1):
            md_content += f"{idx}. [{v['title']}]({v['url']})\n"
        md_content += "\n"

# Target output file
target_path = r"C:\Users\PC\Documents\Google%20Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent\sensebar_ai_agent_videos.md"

os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Markdown generated successfully at: {target_path}")
