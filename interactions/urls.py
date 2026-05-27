from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('review/<int:tmdb_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('favorite/<int:tmdb_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('watchlist/<int:tmdb_id>/', views.toggle_watchlist, name='toggle_watchlist'),
]