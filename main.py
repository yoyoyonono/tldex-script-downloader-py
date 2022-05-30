from tldex import *
from datetime import datetime
import requests

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: tldex-script-downloader <video-id> <output-path>")
        sys.exit(1)
    video = sys.argv[1]
    outPath = sys.argv[2] if len(sys.argv) > 2 else "out.srt"
    url = f'https://holodex.net/api/v2/videos/{video}'
    urlTL = f'{url}/chats?lang=%s&verified=0&moderator=0&vtuber=0&tl=1&limit=100000'
    rMeta = requests.get(url)
    if rMeta.status_code != 200:
        print(f"Error: {rMeta.status_code}")
        sys.exit(1)
    data = rMeta.json()
    meta = VideoMeta(data['status'], datetime.fromisoformat(data['start_actual'][:-1]), datetime.fromisoformat(data['available_at'][:-1]), data['live_tl_count'])
    if not meta.tl_and_count:
        print("Error: No TL data found.")
        sys.exit(1)
    rTL = requests.get(urlTL % list(meta.tl_and_count.keys())[0])
    the_beginning = meta.start_actual or meta.available_at
    script = [Message(line['name'], (datetime.fromtimestamp(int(line['timestamp'])/1000) - the_beginning), line['message']) for line in rTL.json()]
    outString = ""
    for i, m in enumerate(script):
        outString += f"{i}\n{m.timestamp}\n{m.message}\n\n"

    outString = "\n\n".join([f"{i}\n{m.timestamp} --> {(script[i + 1].timestamp) if (i < len(script) - 1) else m.timestamp}\n{m.message}" for i, m in enumerate(script)])
    print(outString)
