from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, UpdateUserForm, ProfileUpdateForm
from .models import Profile
from interactions.models import Review, Favorite, Watchlist

def home_view(request):
    return render(request, 'users/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça seu login.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    user_reviews = Review.objects.filter(user=request.user).select_related('movie')
    user_favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    
    # 🍿 BUSCANDO OS FILMES DA WATCHLIST NO BANCO DE DADOS:
    user_watchlist = Watchlist.objects.filter(user=request.user).select_related('movie')
    
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'bio': profile.bio,
        'location': profile.location,
        'date_joined': request.user.date_joined,
        
        'user_reviews': user_reviews,
        'user_favorites': user_favorites,
        # 🍿 ENVIANDO A VARIÁVEL PARA O HTML:
        'user_watchlist': user_watchlist,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('profile') 
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit_profile.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            remember_me = request.POST.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
            
            return redirect('/movies/') 
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    
    return redirect('/movies/')