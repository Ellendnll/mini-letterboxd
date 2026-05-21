from django.shortcuts import render
from .services import TMDBService

def movie_search(request):
    query = request.GET.get('q', '')
    movies = []
    
    if query:
        service = TMDBService()
        movies = service.search_movies(query)
        
    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'movies/search.html', context)

def movie_detail(request, movie_id):
    service = TMDBService()
    movie = service.get_movie_details(movie_id)
    
    context = {
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)