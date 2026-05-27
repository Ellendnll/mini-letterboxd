from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie
from .models import Review, Favorite, Watchlist
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
            
            if existing:
                messages.success(request, f'Sua avaliação de "{movie.title}" foi atualizada!')
            else:
                messages.success(request, f'Sua review de "{movie.title}" foi salva com sucesso!')
                
            # Verifica se veio da página de perfil ou de detalhes do filme
            if 'profile' in request.META.get('HTTP_REFERER', ''):
                return redirect('/profile/')
            return redirect(f'/movies/{tmdb_id}/')
    else:
        form = ReviewForm(instance=existing)
    
    return render(request, 'interactions/review_form.html', {'form': form, 'movie': movie})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    tmdb_id = review.movie.tmdb_id
    review.delete()
    messages.success(request, 'Review removida com sucesso!')
    
    # Se o usuário deletou estando na página de perfil, mantém ele no perfil
    if 'profile' in request.META.get('HTTP_REFERER', ''):
        return redirect('/profile/')
    return redirect(f'/movies/{tmdb_id}/')

@login_required
def toggle_favorite(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    fav = Favorite.objects.filter(user=request.user, movie=movie).first()
    
    if fav:
        fav.delete()
        messages.info(request, f'"{movie.title}" foi removido dos seus favoritos.')
    else:
        Favorite.objects.create(user=request.user, movie=movie)
        messages.success(request, f'"{movie.title}" foi adicionado aos seus favoritos! ❤️')
    
    return redirect(f'/movies/{tmdb_id}/')

@login_required
def toggle_watchlist(request, tmdb_id):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    wl = Watchlist.objects.filter(user=request.user, movie=movie).first()
    
    if wl:
        wl.delete()
        messages.info(request, f'"{movie.title}" removido da sua lista de "Quero Assistir".')
    else:
        Watchlist.objects.create(user=request.user, movie=movie)
        messages.success(request, f'"{movie.title}" adicionado à sua lista de "Quero Assistir"! 🍿')
    
    return redirect(f'/movies/{tmdb_id}/')