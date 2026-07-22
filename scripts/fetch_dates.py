import subprocess
import json

urls = [
    'https://www.youtube.com/@sensebar/videos',
    'https://www.youtube.com/@sensebar/streams',
    'https://www.youtube.com/@sensebar/shorts'
]

all_videos_dict = {}

for u in urls:
    print(f"Fetching metadata with upload dates from {u}...")
    cmd = ['python', '-m', 'yt_dlp', '-j', '--no-check-certificates', '--dump-single-json', u]
    # dump-single-json gets full metadata including entries with upload_date
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    out, err = proc.communicate()
    
    if out:
        try:
            data = json.loads(out)
            entries = data.get('entries', [])
            print(f"Entries found in {u}: {len(entries)}")
            for item in entries:
                if not item:
                    continue
                v_id = item.get('id')
                title = item.get('title')
                upload_date = item.get('upload_date') # YYYYMMDD
                if v_id and title:
                    all_videos_dict[v_id] = {
                        'id': v_id,
                        'title': title,
                        'url': f'https://www.youtube.com/watch?v={v_id}',
                        'upload_date': upload_date
                    }
        except Exception as e:
            print(f"Error parsing JSON from {u}: {e}")

print(f"Total unique videos fetched with dates: {len(all_videos_dict)}")

videos_list = list(all_videos_dict.values())
with open('all_sensebar_videos_with_dates.json', 'w', encoding='utf-8') as f:
    json.dump(videos_list, f, ensure_ascii=False, indent=2)
