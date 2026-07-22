import urllib.request
import re
import json
import os
import sys

def fetch_youtube_channel_videos(channel_handle="@sensebar"):
    """
    Scrapes public video data from YouTube channel handle without API key requirements.
    """
    url = f"https://www.youtube.com/{channel_handle}/videos"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    print(f"Fetching video data from YouTube channel: {url}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        match = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if match:
            data = json.loads(match.group(1))
            return data
        else:
            print("Could not find ytInitialData in channel HTML.")
            return None
    except Exception as e:
        print(f"Error fetching channel page: {e}")
        return None

def parse_video_items(yt_data):
    """
    Parses video renderer objects into structured video dictionaries.
    """
    videos = []
    try:
        tabs = yt_data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        for tab in tabs:
            tab_renderer = tab.get('tabRenderer', {})
            if tab_renderer.get('selected'):
                content = tab_renderer.get('content', {})
                section_list = content.get('richGridRenderer', {}).get('contents', [])
                for item in section_list:
                    rich_item = item.get('richItemRenderer', {}).get('content', {})
                    video_renderer = rich_item.get('videoRenderer', {})
                    if video_renderer:
                        video_id = video_renderer.get('videoId')
                        title = video_renderer.get('title', {}).get('runs', [{}])[0].get('text', '')
                        if video_id and title:
                            videos.append({
                                'title': title,
                                'id': video_id,
                                'url': f"https://www.youtube.com/watch?v={video_id}"
                            })
    except Exception as e:
        print(f"Error parsing video list: {e}")
    return videos

if __name__ == "__main__":
    yt_data = fetch_youtube_channel_videos("@sensebar")
    if yt_data:
        videos = parse_video_items(yt_data)
        print(f"Successfully extracted {len(videos)} videos.")
        for v in videos[:10]:
            print(f"- {v['title']}: {v['url']}")
        
        # Save output json
        with open("extracted_videos.json", "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
        print("Saved extracted_videos.json")
