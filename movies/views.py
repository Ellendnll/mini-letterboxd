from django.shortcuts import render
from .services import TMDBService

def movie_search(request):
    query = request.GET.get('q','')  
    results = []

    if query:
        tmdb_service = TMDBService()
        results = tmdb_service.search_movies(query)
    
    context = {
        'movies': results
        'query': query
    }
    return render(request, 'movies/search.html', context)

def movie_detail(request, movie_id):
    tmdb_service = TMDBService()
    movie = tmdb_service.get_movie_details(movie_id)

    context = {
        'movie': movie 
    }    
    return render(request, 'movies/movie_detail.html', context)