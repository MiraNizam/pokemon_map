import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime

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
    pokemon_name = Pokemon.objects.get(id=pokemon_id)
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime(), pokemon=pokemon_name)

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

    # user = User.objects.get(username=request.user)
    # manager_orders = Orders.objects.filter(user_id=user.id)
    #
    #
    # for pokemon in pokemon_entities:
    #     if pokemon.id == pokemon_id:
    #         requested_pokemon = pokemon
    #         add_pokemon(
    #             folium_map,
    #             pokemon.latitude,
    #             pokemon.longitude,
    #             request.build_absolute_uri(pokemon.pokemon.image.url)
    #         )
    #     #   return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    #
    # pokemons = Pokemon.objects.all()
    # pokemons_on_page = []
    # for pokemon in pokemons:
    #     pokemon_image_url = None
    #     if pokemon.image:
    #         pokemon_image_url = pokemon.image.url
    #     pokemons_on_page.append({
    #         'pokemon_id': pokemon.id,
    #         'img_url': pokemon_image_url,
    #         'title_ru': pokemon.title,
    #     })
    #
    #     return render(request, 'pokemon.html', context={'map': folium_map._repr_html_(), 'pokemon': pokemon})
