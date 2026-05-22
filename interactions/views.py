from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from movies.models import Movie
from .models import Review, Favorite
from .forms import ReviewForm

@login_required
def rate_movie(request, tmdb_id, rating):
    """Avaliação rápida por estrelas (tipo Letterboxd)"""
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    
    # Pega review existente ou cria nova
    review, created = Review.objects.get_or_create(
        user=request.user,
        movie=movie,
        defaults={'rating': rating, 'comment': ''}
    )
    
    if not created:
        # Se já existe, atualiza a nota
        review.rating = rating
        review.save()
        messages.success(request, f'Nota atualizada para {rating}★')
    else:
        messages.success(request, f'Você avaliou {movie.title} com {rating}★')
    
    return redirect('movies:detail', tmdb_id=movie.tmdb_id)

@login_required
def add_review(request, tmdb_id):
    """Escrever avaliação completa (com comentário)"""
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    existing = Review.objects.filter(user=request.user, movie=movie).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, 'Sua avaliação foi publicada!')
            return redirect('movies:detail', tmdb_id=movie.tmdb_id)
    else:
        form = ReviewForm(instance=existing)
    
    return render(request, 'interactions/review_form.html', {
        'form': form,
        'movie': movie,
        'existing': existing
    })

@login_required
def delete_review(request, review_id):
    """Deletar avaliação"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_id = review.movie.tmdb_id
    review.delete()
    messages.success(request, 'Avaliação removida.')
    return redirect('movies:detail', tmdb_id=movie_id)

@login_required
def toggle_favorite(request, tmdb_id):
    """Favoritar/desfavoritar filme"""
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    fav = Favorite.objects.filter(user=request.user, movie=movie).first()
    
    if fav:
        fav.delete()
        messages.info(request, f'Removido dos favoritos: {movie.title}')
    else:
        Favorite.objects.create(user=request.user, movie=movie)
        messages.success(request, f'Adicionado aos favoritos: {movie.title}')
    
    return redirect('movies:detail', tmdb_id=movie.tmdb_id)

@login_required
def my_reviews(request):
    """Minhas avaliações (página estilo Letterboxd)"""
    reviews = Review.objects.filter(user=request.user).select_related('movie').order_by('-created_at')
    return render(request, 'interactions/my_reviews.html', {'reviews': reviews})

@login_required
def my_favorites(request):
    """Meus favoritos (página estilo Letterboxd)"""
    favorites = Favorite.objects.filter(user=request.user).select_related('movie').order_by('-created_at')
    return render(request, 'interactions/my_favorites.html', {'favorites': favorites})