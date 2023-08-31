import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime())
    for pokemon in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon.latitude,
            pokemon.longitude,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image_url = None
        if pokemon.image:
            pokemon_image_url = pokemon.image.url
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    try:
        pokemon_name = Pokemon.objects.get(id=pokemon_id)
        pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime(), pokemon=pokemon_name)

        for pokemon in pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon.latitude,
                pokemon.longitude,
                request.build_absolute_uri(pokemon.pokemon.image.url)
            )

        pokemon_image_url = pokemon_name.image.url
        pokemon = {
            'pokemon_id': pokemon_name.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon_name.title,
            'description': pokemon_name.description,
            'title_en': pokemon_name.title_en,
            'title_jp': pokemon_name.title_jp,
            'previous_evolution': pokemon_name.previous_evolution,
        }
        if pokemon_name.previous_evolution:
            previous_evolution = {
                'title_ru': pokemon_name.previous_evolution.title,
                'pokemon_id': pokemon_name.previous_evolution.id,
                'img_url': pokemon_name.previous_evolution.image.url,
            }
        else:
            previous_evolution = None

    except ObjectDoesNotExist:
        print("Такого покемона не существует")
    except MultipleObjectsReturned:
        print("Найдено более одного покемона")

    return render(
        request,
        'pokemon.html',
        context={'map': folium_map._repr_html_(), 'pokemon': pokemon, 'previous_evolution': previous_evolution}
    )