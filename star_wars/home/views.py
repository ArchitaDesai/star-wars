from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests

from planets.models import Planet
from movies.models import Movie

def base(request):
    return HttpResponseRedirect('/app/login')

def login(request):
    return render(request, 'base/login.html')


def view_favourites(request):
    favourite_movies = Movie.objects.filter(is_favourite=True)
    favourite_planets = Planet.objects.filter(is_favourite=True)

    return render(request, 'home/favourites.html', 
                    {'favourite_movies': favourite_movies, 'favourite_planets': favourite_planets})


def search_planet(request):
    if request.method == 'POST':
        planet_name = request.POST.get('planet_name')
        print("DATA...............", planet_name)
        if planet_name:
            endpoint = 'https://swapi.dev/api/planets/?search=' 
            url = endpoint + planet_name
            response = requests.get(url)
            data = response.json()
            if data['count'] is not 0:
                print("Data : ", data['results'])
                planet = data['results'][0]
                return render(request, 'home/search_result.html', {'planet': planet})

    return HttpResponseRedirect('/app/home')
