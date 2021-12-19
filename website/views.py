from django.shortcuts import render

# Create your views here.
import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import Video
from django.core.paginator import Paginator
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q='Cricket',
    part='id,snippet',
    maxResults=10,
    type="video",
    order="date",
    publishedAfter="2021-01-01T00:00:00Z"
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for result in search_response.get('items', []):
    if result['id']['kind'] == 'youtube#video':
      video = Video()
      video.title = result['snippet']['title']
      video.description = result['snippet']['description']
      video.thumbnail = result['snippet']['thumbnails']['default']['url']
      video.published_date = result['snippet']['publishedAt']
      video_id = result['id']['videoId']
      obj = Video.objects.all()
      obj = obj.filter(video_id=video_id)
      video.video_id = video_id
      obj.video_id = video_id
      if(obj):
        continue
      else:
        video.save()
      
def index(request):
  youtube_search()
  videos = Video.objects.all().order_by('published_date')
  paginator = Paginator(videos,5)
  pageno = request.GET.get('page')
  videos = paginator.get_page(pageno)
  return render(request, "index.html",{ 'videos': videos})