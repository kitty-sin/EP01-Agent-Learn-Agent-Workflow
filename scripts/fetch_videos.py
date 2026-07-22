import subprocess
import json

cmd = ['python', '-m', 'yt_dlp', '--flat-playlist', '-j', '--no-check-certificates', 'https://www.youtube.com/@sensebar/videos']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

videos = []
for line in proc.stdout:
    line = line.strip()
    if line:
        try:
            item = json.loads(line)
            v_id = item.get('id')
            title = item.get('title')
            if v_id and title:
                videos.append({
                    'id': v_id,
                    'title': title,
                    'url': f'https://www.youtube.com/watch?v={v_id}'
                })
        except Exception as e:
            pass

proc.wait()
print(f"Total videos fetched from @sensebar: {len(videos)}")

with open('all_sensebar_videos.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)
