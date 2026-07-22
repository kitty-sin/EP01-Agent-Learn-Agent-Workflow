import subprocess
import json
import os

urls = [
    'https://www.youtube.com/@sensebar/videos',
    'https://www.youtube.com/@sensebar/streams',
    'https://www.youtube.com/@sensebar/shorts'
]

video_data_dict = {}

for u in urls:
    print(f"Fetching dates from {u}...")
    cmd = [
        'python', '-m', 'yt_dlp',
        '--print', '%(id)s\t%(upload_date)s\t%(title)s',
        '--no-check-certificates',
        u
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    count = 0
    for raw_line in proc.stdout:
        line = raw_line.decode('utf-8', errors='replace').strip()
        if line:
            parts = line.split('\t')
            if len(parts) >= 3:
                v_id, upload_date, title = parts[0], parts[1], parts[2]
                if v_id not in video_data_dict:
                    video_data_dict[v_id] = {
                        'id': v_id,
                        'upload_date': upload_date, # YYYYMMDD string, e.g. 20250315 or 20241220
                        'title': title,
                        'url': f'https://www.youtube.com/watch?v={v_id}'
                    }
                    count += 1
    proc.wait()
    print(f"Fetched {count} video metadata from {u}")

print(f"Total unique videos fetched: {len(video_data_dict)}")

target_path = r'c:\Users\PC\Documents\Google%20Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent\all_sensebar_videos_with_dates.json'
with open(target_path, 'w', encoding='utf-8') as f:
    json.dump(list(video_data_dict.values()), f, ensure_ascii=False, indent=2)

print("Saved all_sensebar_videos_with_dates.json to", target_path)
