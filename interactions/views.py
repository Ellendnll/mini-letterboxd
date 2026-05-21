from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie
from .models import Review, Favorite
from .forms import ReviewForm

@login_required
def add_review(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    existing = Review.objects.filter(user=request.user, movie=movie).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, 'Review salva com sucesso!')
            return redirect('movies:detail', tmdb_id=movie.tmdb_id)
    else:
        form = ReviewForm(instance=existing)
    
    return render(request, 'interactions/review_form.html', {'form': form, 'movie': movie})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    tmdb_id = review.movie.tmdb_id
    review.delete()
    messages.success(request, 'Review removida!')
    return redirect('movies:detail', tmdb_id=tmdb_id)

@login_required
def toggle_favorite(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    fav = Favorite.objects.filter(user=request.user, movie=movie).first()
    
    if fav:
        fav.delete()
        messages.info(request, f'"{movie.title}" removido dos favoritos')
    else:
        Favorite.objects.create(user=request.user, movie=movie)
        messages.success(request, f'"{movie.title}" adicionado aos favoritos')
    
    return redirect('movies:detail', tmdb_id=movie.tmdb_id)