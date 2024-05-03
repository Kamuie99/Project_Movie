from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_safe
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Movie, Genre
from django.conf import settings
import requests

API_URL = settings.API_URL
# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    context = {
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movies/index.html', context)


def filter_genre(request):
    genre_id = request.GET.get('genre_id')
    if genre_id:
        movies = Movie.objects.filter(genres__id=genre_id).values('id', 'title', 'overview', 'release_date', 'popularity', 'vote_count', 'vote_average', 'poster_path')
    else:
        movies = Movie.objects.all().values('id', 'title', 'overview', 'release_date', 'popularity', 'vote_count', 'vote_average', 'poster_path')

    return JsonResponse(list(movies), safe=False)


# @require_safe
require_http_methods(['GET'])
def recommended(request):
    years = [i for i in range(1990, 2024)]
    genres = Genre.objects.all()

    # response = requests.get(API_URL).json().get('movieListResult')['movieList']
    # print(response)
    # return JsonResponse(list(response), safe=False)
    context = {
        'years': years,
        'genres': genres,
    }
    return render(request, 'movies/recommended.html', context)
