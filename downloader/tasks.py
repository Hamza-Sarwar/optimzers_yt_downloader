# downloader/tasks.py
from celery import Celery
import yt_dlp
import logging

logging.getLogger().setLevel(logging.INFO)
celery_app = Celery('tasks', broker='redis://localhost:6379/')

SAVE_PATH = './data'

@celery_app.task
def download_channel_videos(channel_id):
    ydl_opts = {
        'ignoreerrors': True,
        'format': 'best',
        'outtmpl': SAVE_PATH + f'/{channel_id}' + '/%(title)s.%(ext)s',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/{channel_id}'])
