import os

from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.__api_key: str = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__video_response = self.__youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=video_id
                                       ).execute()
        self.__get_exeption()

    def __get_exeption(self):
        """Если id было ошибочным, все данные кроме id вернутся как None"""
        try:
            self.title = self.__video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.title = self.__video_response['items'][0]['snippet']['title']
            self.url = 'http://www.moscowpython.ru/meetup/14/gil-and-python-why/'
            self.view_count = self.__video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.__video_response['items'][0]['statistics']['likeCount']
            return self.title, self.url, self. view_count, self.like_count

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
