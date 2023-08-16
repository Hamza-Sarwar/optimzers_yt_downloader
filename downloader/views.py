# downloader/views.py
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import download_channel_videos

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
def download_video(request):
    if request.method == 'POST':
        video_link = request.POST.get('video_link')
        # Validate and process the link
        # Perform downloading using youtube_dl
        # Return appropriate response

@csrf_exempt
def download_playlist(request):
    if request.method == 'POST':
        playlist_link = request.POST.get('playlist_link')
        # Validate and process the link
        # Perform downloading using youtube_dl
        # Return appropriate response

