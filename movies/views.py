from django.shortcuts import render, get_object_or_404
from .services import TMDBService
from interactions.models import Review, Favorite, Watchlist
from .models import Movie 

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
    """
    Função principal de detalhes: Puxa os dados técnicos do filme via API 
    e mescla com as interações (reviews/favoritos) salvas no banco de dados.
    """
    service = TMDBService()
    movie_api = service.get_movie_details(movie_id)

    #  Proteção de Segurança: Se a API falhar ou não retornar nada, cria um dicionário padrão
    if not movie_api:
        movie_api = {'id': movie_id, 'title': 'Filme não encontrado'}
    
    #  Garante ou cria o registro do filme no nosso banco local usando o ID do TMDB
    # Passamos strings vazias '' como padrão caso a API traga campos nulos (Evita IntegrityError)
    movie_db, created = Movie.objects.get_or_create(
        tmdb_id=movie_id,
        defaults={
            'title': movie_api.get('title', 'Filme sem título')
        }
    )
    
    #  Puxa todos os comentários desse filme específicos do banco
    reviews = Review.objects.filter(movie=movie_db).select_related('user')
    
    # Valores padrão para usuários não logados
    user_rating = None
    is_favorited = False
    
    is_in_watchlist = False
    

    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, movie=movie_db).first()
        if user_review:
            user_rating = user_review.rating
        is_favorited = Favorite.objects.filter(user=request.user, movie=movie_db).exists()
        
        
        is_in_watchlist = Watchlist.objects.filter(user=request.user, movie=movie_db).exists()
    
    context = {
        'movie': movie_api,       # Dados da API (capa, sinopse, ano)
        'movie_db': movie_db,     # Instância do banco de dados para os formulários
        'reviews': reviews,       # Lista de comentários
        'user_rating': user_rating,
        'is_favorited': is_favorited,
        'is_in_watchlist': is_in_watchlist,
    }
    
    return render(request, 'movies/movie_detail.html', context)