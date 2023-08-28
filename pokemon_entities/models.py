from django.db import models # noqa F401
from datetime import datetime

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    image = models.ImageField(upload_to="images", verbose_name="Картинка")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(max_length=100, verbose_name="Широта")
    longitude = models.FloatField(max_length=100, verbose_name="Долгота")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    appeared_at = models.DateTimeField(default=datetime.now(), verbose_name="Появляется")
    disappeared_at = models.DateTimeField(default=datetime.now(), verbose_name="Исчезает")
    level = models.IntegerField(blank=True, null=True,  default=None, verbose_name="Уровень")
    health = models.IntegerField(blank=True, null=True, default=None, verbose_name="Здоровье")
    strength = models.IntegerField(blank=True, null=True, default=None, verbose_name="Сила")
    defence = models.IntegerField(blank=True, null=True, default=None, verbose_name="Защита")
    stamina = models.IntegerField(blank=True, null=True, default=None, verbose_name="Выносливость")