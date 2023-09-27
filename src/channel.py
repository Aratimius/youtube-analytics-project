import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__api_key: str = os.getenv('YT_API_KEY')
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)
        self.__channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()


    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, new_channel_id):
        print("AttributeError: property 'channel_id' of 'Channel' object has no setter")

    @property
    def title(self):
        return self.__channel['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.__channel['items'][0]['snippet']['description']

    @property
    def video_count(self):
        return self.__channel['items'][0]['statistics']['videoCount']

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def subscriber_count(self):
        return self.__channel['items'][0]['statistics']['subscriberCount']

    @property
    def view_count(self):
        return self.__channel['items'][0]['statistics']['viewCount']

    def to_json(self, json_file):
        """Сохраняем данные атрибутов словаря в json-файл"""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'videoCount': self.video_count,
            'url': self.url,
            'viewCount': self.view_count,
            'subscriberCount': self.subscriber_count
                }
        with open(json_file, 'w') as j_file:
            json.dump(data, j_file)

    def get_service(self):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=self.__api_key)
        return youtube
