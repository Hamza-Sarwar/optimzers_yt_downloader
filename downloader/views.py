# downloader/views.py
import logging

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import DownloadForm
from .tasks import download_channel_videos
import yt_dlp
import re
@csrf_exempt
def download_channel(request):
    if request.method == 'GET':
        channel_link = 'https://www.youtube.com/@AskGanjiswag'
        channel_id = channel_link.split('/')[-1]  # Define a function to extract channel_id from the link
        if channel_id:
            download_channel_videos.apply_async(args=(channel_id,))  # Pass channel_id as an argument
            return HttpResponse(True)
        else:
            return HttpResponse("Invalid channel link provided")

@csrf_exempt
# def download_video(request):
#     # Create a yt-dlp options object
#     ydl_opts = {}
#     video_url = 'https://www.youtube.com/watch?v=jLHpTVLifMk'
#     # Create a yt-dlp object with the options
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(video_url, download=True)
#         video_title = info_dict.get('title', None)
#         logging.info(info_dict.keys())
#         logging.info(info_dict.get('availability'))
#         logging.info(info_dict.get('requested_formats'))
#         logging.info(info_dict.get('format'))
#         logging.info(info_dict.get('filesize_approx'))
#     # response = HttpResponse(content_type='application/force-download')
#     # response['Content-Disposition'] = f'attachment; filename="{video_title}.mp4"'
#     #
#     # video_path = f'./{video_title}.mp4'  # Change this to the actual path where the video is downloaded
#     # with open(video_path, 'rb') as video_file:
#     #     response.write(video_file.read())
#
#     return HttpResponse({"info": info_dict})
def download_video(request):
    global context
    form = DownloadForm(request.POST or None)

    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        if not re.match(regex, video_url):
            return HttpResponse('Enter correct url.')

        ydl_opts = {}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    video_url, download=False)
            video_audio_streams = []
            for m in meta['requested_formats']:
                file_size = m['filesize']
                if file_size is not None:
                    file_size = f'{round(int(file_size) / 1000000, 2)} mb'

                resolution = 'Audio'
                if m['height'] is not None:
                    resolution = f"{m['height']}x{m['width']}"
                video_audio_streams.append({
                    'resolution': resolution,
                    'extension': m['ext'],
                    'file_size': file_size,
                    'video_url': m['url']
                })
            video_audio_streams = video_audio_streams[::-1]
            context = {
                'form': form,
                'title': meta.get('title', None),
                'streams': video_audio_streams,
                'description': meta.get('description'),
                'likes': f'{int(meta.get("like_count", 0)):,}',
                'dislikes': f'{int(meta.get("dislike_count", 0)):,}',
                'thumb': meta.get('thumbnails')[3]['url'],
                'duration': round(int(meta.get('duration', 1)) / 60, 2),
                'views': f'{int(meta.get("view_count")):,}'
            }
            return render(request, 'home.html', context)
        except Exception as error:
            return HttpResponse(error.args[0])
    return render(request, 'home.html', {'form': form})

@csrf_exempt
def download_playlist(request):
    if request.method == 'POST':
        playlist_link = request.POST.get('playlist_link')
        # Validate and process the link
        # Perform downloading using youtube_dl
        # Return appropriate response

