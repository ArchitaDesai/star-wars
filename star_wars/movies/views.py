from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests

from .models import Movie

def format(data):
    """ ToDo:
        - Create common helper functions to be used across modules (movies & planets)
    """
    existing_movie_swapi_ids = list(Movie.objects.values_list('swapi_id', flat=True))
    existing_movie_favourites = list(Movie.objects.values_list('is_favourite', flat=True))
    movies = data['results']
    formatted_movies = []
    for movie in movies:
        movie_url = movie['url']
        swapi_id = int(movie_url.split("api/films/",1)[1].split('/',1)[0])
        try:
            existing_movie_index = existing_movie_swapi_ids.index(swapi_id)
            is_favourite = existing_movie_favourites[existing_movie_index]
        except ValueError:
            is_favourite = False
        formatted_movie = {
            'swapi_id': swapi_id,
            'title': movie['title'],
            'is_favourite': is_favourite,
            'opening_crawl': movie['opening_crawl']
        }
        formatted_movies.append(formatted_movie)

    return formatted_movies


def list_movies(request):
    response = requests.get('https://swapi.dev/api/films/')
    data = response.json()
    formatted_movies = format(data)
    return render(request, 'movies/list.html', {'movies': formatted_movies})


def update_favourite(request, swapi_id, movie_title):
    swapi_int = int(swapi_id)
    try:
        movie = Movie.objects.get(swapi_id=swapi_int)
        movie.is_favourite = not movie.is_favourite # ToDo: Use 'Case' to invert negation efficiently
        movie.save()
    except Movie.DoesNotExist:
        Movie.objects.create(swapi_id=swapi_int, title=movie_title, is_favourite=True)

    return HttpResponseRedirect('/app/movies')
