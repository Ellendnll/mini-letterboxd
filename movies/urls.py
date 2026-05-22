from django.urls import path
from . import views

 Define o nome do aplicativo para organização das URLs do Django
app_name = 'movies'

urlpatterns = [
     Rota para a página de busca: /movies/
    path('', views.movie_search, name='movie_search'),
    
     Rota para os detalhes do filme (recebe o ID do TMDB na URL): /movies/123/
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
]