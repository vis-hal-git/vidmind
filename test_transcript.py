import os, httpx
from dotenv import load_dotenv
import database as db

load_dotenv(override=True)
key = os.getenv('SUPADATA_API_KEY')

try:
    videos = db.get_all_sessions()
    session = videos[-1]
    vids = db.get_session_videos(session['id'])
    last_vid = vids[-1]['video_id']
except Exception as e:
    print('Failed to get last video', e)
    last_vid = 'WruTz1y6g2A'

print(f'Testing video: {last_vid}')
r = httpx.get('https://api.supadata.ai/v1/youtube/transcript', headers={'x-api-key': key}, params={'videoId': last_vid}, timeout=60.0)
data = r.json()
if 'content' in data:
    text = ' '.join([c['text'] for c in data['content']])
    print(f'Supadata transcript length: {len(text)} characters, {len(data["content"])} segments')
else:
    print('Supadata Error:', data)

from youtube_transcript_api import YouTubeTranscriptApi
try:
    yt_data = YouTubeTranscriptApi.get_transcript(last_vid)
    yt_text = ' '.join([c['text'] for c in yt_data])
    print(f'Youtube transcript length: {len(yt_text)} characters, {len(yt_data)} segments')
except Exception as e:
    print('Youtube Error:', e)
