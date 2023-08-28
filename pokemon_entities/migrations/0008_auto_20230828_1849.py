# Generated by Django 3.1.14 on 2023-08-28 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0007_auto_20230828_1834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='text',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 18, 49, 14, 282724), verbose_name='Появляется'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 28, 18, 49, 14, 282744), verbose_name='Исчезает'),
        ),
    ]