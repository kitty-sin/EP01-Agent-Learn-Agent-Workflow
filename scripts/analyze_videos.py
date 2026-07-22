import json
import re

with open('all_sensebar_videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total videos in channel: {len(videos)}")

# Keywords criteria
keywords = [
    'claude', 'codex', 'antigravity', 'anti gravity', 'opencode',
    'agent', 'agents', 'chatgpt', 'gpt', 'google', 'gemini',
    'notebooklm', 'notebook lm', 'ai', '簡報', '基本功', '應用', '工具',
    'felo', 'canvas', 'obsidian', 'supabase', 'firebase', 'github', 'mcp'
]

matching_videos = []
non_matching_videos = []

for v in videos:
    title = v['title']
    title_lower = title.lower()
    
    # Check if title matches any keyword
    matched = any(kw in title_lower for kw in keywords)
    
    if matched:
        matching_videos.append(v)
    else:
        non_matching_videos.append(v)

print(f"Matching videos count: {len(matching_videos)}")
print(f"Non-matching videos count: {len(non_matching_videos)}")

print("\nSample Non-matching titles:")
for v in non_matching_videos[:20]:
    print("-", v['title'])
