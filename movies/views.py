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


def detail(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    reviews = Review.objects.filter(movie=movie).select_related('user')
    
    # Para mostrar a nota do usuário atual
    user_rating = None
    is_favorited = False
    
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, movie=movie).first()
        if user_review:
            user_rating = user_review.rating
        is_favorited = Favorite.objects.filter(user=request.user, movie=movie).exists()
    
    return render(request, 'movies/detail.html', {
        'movie': movie,
        'reviews': reviews,
        'user_rating': user_rating,
        'is_favorited': is_favorited,
})
    