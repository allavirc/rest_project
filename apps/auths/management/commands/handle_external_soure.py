from typing import Any
from datetime import datetime
from django.core.management import BaseCommand
import requests
from requests import Response
from requests import get
from main import models
from main.models import Anime, Genre
from rest_framework import request


class Command(BaseCommand):
    """Get data from extremal sourse and handle it."""

    help = "Get data from extremal sourse and handle it."

    URL = 'https://raw.githubusercontent.com/asarode/anime-list/master/data/data.json'

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def __convert_text_to_date(
            self,
            start_date: str
    ) -> datetime:
        """Converts text to datetime obj."""

        month_map: dict[str, str] = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12',
        }
        published: str = start_date.split(' (')[0]

        month: str = published[0:3]  # 'Apr'
        month_num: str = month_map[month]  # '04'

        custom_published: str = published.replace(
            month,
            month_num
        )
        month_day: str
        year: str
        time: str
        try:
            month_day, year, time = custom_published.split(',')
        except ValueError:
            month_day, year = custom_published.split(',')
            time = '00:00'

        year = year.replace(' ', '')
        time = time.replace(' ', '')

        _: str
        day: str
        _, day = month_day.split(' ')

        day_str: str = day
        if len(day) == 1:
            day_str = ''.join(
                [
                    '0',
                    day
                ]
            )
        date_time_str: str = f'{day_str}/{month_num}/{year} {time}'

        date: datetime = datetime.strptime(
            date_time_str,
            '%d/%m/%Y %H:%M'
        )
        return date

    def _generate_data(self) -> None:

        # Fetching data from source
        response: models.Response = get(self.URL)

        if response.status_code != 200:
            return None

        # Converting response to json
        data: list[dict[str, Any]] = response.json()

        obj: dict[str, Any]
        for obj in data:
            studio: str = obj.get('studio')
            genres: list[str] = obj['genres']
            rating: int = obj['hype']
            description: str = obj['description']
            link: str = obj['title']['link']
            name: str = obj['title']['text']

            start_date: datetime = \
                self.__convert_text_to_date(obj['start_date'])

            print('Done...')
            anime_dict: dict = {
                'studio': studio,
                'rating': rating,
                'description': description,
                'link': link,
                'name': name,
            }
            anime = Anime.objects.get_or_create(**anime_dict)
            for i in genres:
                try:
                    g = Genre.objects.create(name=i)
                    g.anime.set(anime)
                except Exception as e:
                    print(f'[ERROR GENERATE] {e}')

            # print(f"Genres- {obj.get('studio')}")
            # print(f"Genres- {obj['genres']}")
            # print(f"Genres- {obj['hype']}")
            # print(f"Genres- {obj['description']}")
            # print(f"Genres- {obj['title']}")
            # print(f"Genres- {obj['title']['link']}")
            # print(f"Genres- {obj['title']['text']}")



    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling"""

        start: datetime = datetime.now()

        self._generate_data()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now() - start).total_seconds())
        )
