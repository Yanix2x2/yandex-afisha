from django.db import models


class Place(models.Model):
    title = models.CharField("Название мероприятия", max_length=200)
    description_short = models.TextField("Короткие описание", blank=True)
    description_long = models.TextField("Полное описание", blank=True)
    longitude = models.FloatField("Долгота")
    latitude = models.FloatField("Широта")

    def __str__(self):
        return self.title
