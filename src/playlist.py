import os
import isodate

from datetime import timedelta
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.__playlist_response = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.__playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]

        self.__video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.__video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        """Возвращает общую длительность видеороликов в плейлисте"""

        # Создаем переменную типа timedelta для сложения длительности видеороликов
        durations = timedelta(hours=0, minutes=0, seconds=0)
        for video in self.__video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations = durations + duration
        return durations

    @property
    def url(self):
        return f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def title(self):
        return self.__playlist_response['items'][0]['snippet']['title']

    def show_best_video(self):
        """Возвращает ссылку на самое залайканое видео из плейлиста"""
        best_video = self.__video_response['items'][0]
        for video in self.__video_response['items']:
            if video['statistics']['likeCount'] > best_video['statistics']['likeCount']:
                best_video = video
        return f"https://youtu.be/{best_video['id']}"
