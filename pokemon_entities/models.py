from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to="images")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(max_length=100)
    longitude = models.FloatField(max_length=100)
