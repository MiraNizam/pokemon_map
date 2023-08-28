# Generated by Django 3.1.14 on 2023-08-28 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20230828_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 18, 34, 3, 868876), verbose_name='Появляется'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 18, 34, 3, 868896), verbose_name='Исчезает'),
        ),
    ]