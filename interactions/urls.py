from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    # Avaliação rápida por estrelas
    path('rate/<int:tmdb_id>/<int:rating>/', views.rate_movie, name='rate_movie'),
    
    # Review completa com comentário
    path('review/<int:tmdb_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    # Favoritos
    path('favorite/<int:tmdb_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # Páginas do usuário
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
]