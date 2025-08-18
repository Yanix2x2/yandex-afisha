from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse

from places.models import Place


def get_place(request, place_id) -> JsonResponse:
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        id=place_id
        )

    images = place.images.all()
    image_urls = [image.picture.url for image in images]

    properties = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": { 
            "lng": place.longitude,
            "lat": place.latitude,
        }
    }

    return JsonResponse(properties, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def index(request):
    places = Place.objects.all()
    features = []

    for place in places:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude]
                },
                "properties": {
                    "title": place.title,
                    "placeId": place.id,
                    "detailsUrl": reverse('get_place', args=[place.id])
                }
            }
        )

    places_geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    context = {
        "places_geojson": places_geojson
    }

    return render(request, 'index.html', context)
