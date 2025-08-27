from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import IntegrityError
import requests
from requests.exceptions import HTTPError, ConnectionError
import json

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Загружает данные в базу данных из JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL of JSON file')

    def handle(self, *args, **options):
        json_url = options['json_url']
        response = requests.get(json_url)
        response.raise_for_status()
        raw_place = json.loads(response.text)

        try:
            place, created = Place.objects.get_or_create(
                title=raw_place['title'],
                longitude=float(raw_place['coordinates']['lng']),
                latitude=float(raw_place['coordinates']['lat']),

                defaults={
                    'short_description': raw_place['description_short'],
                    'long_description': raw_place['description_long'],
                }
            )

        except IntegrityError as error:
            print(f"IntegrityError for place {raw_place['title']}: {error}")

        for img_url in raw_place['imgs']:
            try:
                response = requests.get(img_url)
                response.raise_for_status()

                img_name = img_url.split('/')[-1]
                image = Image.objects.create(place=place)
                image.picture.save(img_name, ContentFile(response.content))

            except HTTPError as http_err:
                print(f"HTTP ошибка при загрузке {img_url}: {http_err}")
                continue

            except ConnectionError as conn_err:
                print(f"Ошибка соединения при загрузке {img_url}: {conn_err}")
                continue

        msg = self.style.SUCCESS(f'Successfully loaded place "{place.title}"')
        self.stdout.write(msg)
