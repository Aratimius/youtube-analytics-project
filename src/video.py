import os

from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.__video_id = video_id
        self.__api_key: str = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=video_id
                                       ).execute()

    def __str__(self):
        return self.video_title
    @property
    def video_id(self):
        return self.__video_id

    @property
    def video_title(self):
        return self.__video_response['items'][0]['snippet']['title']

    @property
    def url(self):
        return 'http://www.moscowpython.ru/meetup/14/gil-and-python-why/'

    @property
    def view_count(self):
        return self.__video_response['items'][0]['statistics']['viewCount']

    @property
    def like_count(self):
        return self.__video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
