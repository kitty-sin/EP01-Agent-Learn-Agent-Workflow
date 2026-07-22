import subprocess
import json

urls = [
    'https://www.youtube.com/@sensebar/videos',
    'https://www.youtube.com/@sensebar/streams',
    'https://www.youtube.com/@sensebar/shorts'
]

all_videos_dict = {}

for u in urls:
    print(f"Fetching from {u}...")
    cmd = ['python', '-m', 'yt_dlp', '--flat-playlist', '-j', '--no-check-certificates', u]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    
    count = 0
    for line in proc.stdout:
        line = line.strip()
        if line:
            try:
                item = json.loads(line)
                v_id = item.get('id')
                title = item.get('title')
                if v_id and title:
                    all_videos_dict[v_id] = {
                        'id': v_id,
                        'title': title,
                        'url': f'https://www.youtube.com/watch?v={v_id}'
                    }
                    count += 1
            except Exception as e:
                pass
    proc.wait()
    print(f"Fetched {count} videos from {u}")

print(f"Total unique videos across all tabs: {len(all_videos_dict)}")

videos_list = list(all_videos_dict.values())
with open('all_sensebar_videos.json', 'w', encoding='utf-8') as f:
    json.dump(videos_list, f, ensure_ascii=False, indent=2)
