import subprocess
import json
import os

yt_dlp_bin = r"C:\Users\PC\AppData\Local\Microsoft\WinGet\Packages\yt-dlp.yt-dlp_Microsoft.Winget.Source_8wekyb3d8bbwe\yt-dlp.exe"

cmd = [
    yt_dlp_bin,
    "--no-check-certificates",
    "--flat-playlist",
    "-J",
    "https://www.youtube.com/@sensebar/videos"
]

print(f"Executing {yt_dlp_bin}...")
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if res.returncode != 0:
    print("yt-dlp error:", res.stderr)
    exit(1)

data = json.loads(res.stdout)
entries = data.get("entries", [])
print(f"Total videos fetched: {len(entries)}")

# Target keywords requested by user: claude ai, codex, antigravity, opencode, ai agent, agent
keywords = ["claude", "codex", "antigravity", "opencode", "agent", "ai"]

matched = []
all_videos = []

for entry in entries:
    title = entry.get("title", "")
    video_id = entry.get("id")
    url = f"https://www.youtube.com/watch?v={video_id}"
    all_videos.append({"title": title, "url": url, "id": video_id})
    
    title_lower = title.lower()
    if any(k in title_lower for k in keywords):
        matched.append({"title": title, "url": url, "id": video_id})

print(f"\nMatched count: {len(matched)}")

json_out = r"C:\Users\PC\.gemini\antigravity\brain\d1555396-20ff-4bcd-b436-84c71dfd00cd\scratch\videos.json"
with open(json_out, "w", encoding="utf-8") as f:
    json.dump({"matched": matched, "all": all_videos}, f, ensure_ascii=False, indent=2)

print("Saved to JSON.")
