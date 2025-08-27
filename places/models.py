from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField("Название мероприятия", max_length=200)
    short_description = models.TextField("Короткое описание", blank=True)
    long_description = HTMLField("Полное описание", blank=True)
    longitude = models.FloatField("Долгота")
    latitude = models.FloatField("Широта")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                    fields=['title', 'longitude', 'latitude'],
                    name='unique_title_coordinates'
                ),
        ]

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    picture = models.ImageField("Картинка", upload_to="")
    serial_number = models.PositiveIntegerField("Порядковый номер", default=0)

    class Meta:
        ordering = ["serial_number"]
        indexes = [
            models.Index(fields=['place', 'serial_number']),
        ]

    def __str__(self):
        return f'{self.serial_number} {self.place.title}'
