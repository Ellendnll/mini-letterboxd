from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from interactions.models import Review, Favorite

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado! Faça login.')
            return redirect('users:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # Busca as reviews e favoritos do usuário (sua parte integrada)
    user_reviews = Review.objects.filter(user=request.user).select_related('movie')
    user_favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    
    context = {
        'user_reviews': user_reviews,
        'user_favorites': user_favorites,
    }
    return render(request, 'users/profile.html', context)