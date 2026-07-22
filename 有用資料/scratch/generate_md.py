import json
import os

json_path = r"C:\Users\PC\.gemini\antigravity\brain\d1555396-20ff-4bcd-b436-84c71dfd00cd\scratch\videos.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

all_videos = data["all"]

# Let's inspect titles and categorize accurately
claude_list = []
codex_list = []
antigravity_list = []
opencode_list = []
agent_list = []
ai_coding_list = []
other_ai_list = []

for v in all_videos:
    title = v["title"]
    url = v["url"]
    t_lower = title.lower()

    if "claude" in t_lower or "sonnet" in t_lower or "opus" in t_lower:
        claude_list.append(v)
    elif "codex" in t_lower or "code interpreter" in t_lower:
        codex_list.append(v)
    elif "antigravity" in t_lower or "gemini" in t_lower:
        antigravity_list.append(v)
    elif "opencode" in t_lower or "open code" in t_lower:
        opencode_list.append(v)
    elif "agent" in t_lower or "智能體" in t_lower or "代理" in t_lower:
        agent_list.append(v)
    elif any(k in t_lower for k in ["code", "coding", "cursor", "bolt", "windsurf", "replit", "v0", "gpt", "chatgpt", "deep research", "ai"]):
        ai_coding_list.append(v)
    else:
        other_ai_list.append(v)

print(f"Claude: {len(claude_list)}")
print(f"Codex: {len(codex_list)}")
print(f"Antigravity/Gemini: {len(antigravity_list)}")
print(f"OpenCode: {len(opencode_list)}")
print(f"Agent: {len(agent_list)}")
print(f"AI Coding/GPT: {len(ai_coding_list)}")

# Let's print out all titles in all_videos so we can see the exact titles in console/log
with open(r"C:\Users\PC\.gemini\antigravity\brain\d1555396-20ff-4bcd-b436-84c71dfd00cd\scratch\all_titles_utf8.txt", "w", encoding="utf-8") as f:
    for v in all_videos:
        f.write(f"{v['title']} ||| {v['url']}\n")

print("Wrote all titles to txt.")
