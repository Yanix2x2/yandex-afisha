from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import requests
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
        item = json.loads(response.text)

        place, created = Place.objects.get_or_create(
            title=item['title'],
            description_short=item['description_short'],
            description_long=item['description_long'],
            longitude=float(item['coordinates']['lng']),
            latitude=float(item['coordinates']['lat'])
        )

        for img_url in item['imgs']:
            response = requests.get(img_url)
            img_name = img_url.split('/')[-1]
            image = Image(place=place)
            image.picture.save(img_name, ContentFile(response.content), save=True)

        msg = self.style.SUCCESS(f'Successfully loaded place "{place.title}"')
        self.stdout.write(msg)
