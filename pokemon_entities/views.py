import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import get_object_or_404

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


def check_image(pokemon):
    """The function receives QuerySet object and check the image, it there is not image it put Default meaning."""
    pokemon_image_url = DEFAULT_IMAGE_URL
    if pokemon.image:
        pokemon_image_url = pokemon.image.url
    return pokemon_image_url


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    localtime_now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime_now, disappeared_at__gt=localtime_now)
    for pokemon in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon.latitude,
            pokemon.longitude,
            request.build_absolute_uri(check_image(pokemon.pokemon))
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image_url = check_image(pokemon)
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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    localtime_now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime_now, disappeared_at__gt=localtime_now, pokemon=pokemon)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(check_image(pokemon_entity.pokemon))
        )

    pokemon_description = {
        'pokemon_id': pokemon.id,
        'img_url': check_image(pokemon),
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'previous_evolution': pokemon.previous_evolution,
        'next_evolution': pokemon.next_evolutions.first()
    }
    return render(
        request,
        'pokemon.html',
        context={'map': folium_map._repr_html_(), 'pokemon': pokemon_description})