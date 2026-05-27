from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
def profile_view(request, username=None):
    # Define de quem é o perfil que estamos visitando
    if username is None:
        target_user = request.user  
        is_own_profile = True
    else:
        target_user = get_object_or_404(User, username=username)
        is_own_profile = (target_user == request.user)

    # Busca os perfis usando a classe Profile diretamente (soma os avisos do .profile)
    profile, created = Profile.objects.get_or_create(user=target_user)
    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Checagem de relacionamento usando a estrutura que o editor conhece
    is_following = my_profile.following.filter(pk=profile.pk).exists()
    
    # Lógica de Privacidade
    is_locked = (not is_own_profile) and profile.is_private and (not is_following)

    # Buscar os dados
    if not is_locked:
        user_reviews = Review.objects.filter(user=target_user).select_related('movie')
        user_favorites = Favorite.objects.filter(user=target_user).select_related('movie')
        user_watchlist = Watchlist.objects.filter(user=target_user).select_related('movie')
    else:
        user_reviews = Review.objects.none()
        user_favorites = Favorite.objects.none()
        user_watchlist = Watchlist.objects.none()

    #Tratamento seguro para contar os seguidores sem confundir o linter do editor
    try:
        followers_count = profile.followers.count()
    except AttributeError:
        #Alternativa via query direta caso o editor bloqueie a leitura dinâmica
        followers_count = Profile.objects.filter(following=profile).count()

    context = {
        'target_user': target_user,
        'username': target_user.username,
        'email': target_user.email,
        'bio': profile.bio,
        'location': profile.location,
        'date_joined': target_user.date_joined,
        'is_private': profile.is_private,
        
        # Variáveis de controle para o HTML
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'is_locked': is_locked,
        
        # Contadores e listas
        'user_reviews': user_reviews,
        'user_favorites': user_favorites,
        'user_watchlist': user_watchlist,
        
        # Contadores de seguidores e seguindo
        'followers_count': followers_count,
        'following_count': profile.following.count(),
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

@login_required
def follow_toggle_view(request, username):
    """View para seguir ou deixar de seguir um usuário"""
    user_to_modify = get_object_or_404(User, username=username)
    
    if user_to_modify == request.user:
        messages.error(request, "Você não pode seguir a si mesmo!")
        return redirect('profile')

    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    target_profile, _ = Profile.objects.get_or_create(user=user_to_modify)

    if target_profile in my_profile.following.all():
        my_profile.following.remove(target_profile)
        messages.success(request, f"Você deixou de seguir @{username}.")
    else:
        my_profile.following.add(target_profile)
        messages.success(request, f"Agora você está seguindo @{username}!")

    return redirect('/profile/' + username + '/')

@login_required
def user_search_view(request):
    """View para pesquisar usuários cadastrados no sistema"""
    query = request.GET.get('q', '').strip()
    users_found = []

    if query:
        users_found = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)

    context = {
        'users_found': users_found,
        'query': query,
    }
    return render(request, 'users/user_search.html', context)

@login_required
def user_connections_view(request, username, list_type):
    """View para listar os seguidores ou quem o usuário está seguindo"""
    target_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=target_user)
    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Checa se o perfil está trancado para o usuário atual
    is_own_profile = (target_user == request.user)
    is_following = my_profile.following.filter(pk=profile.pk).exists()
    is_locked = (not is_own_profile) and profile.is_private and (not is_following)
    
    # Bloqueia o acesso se a conta for privada e você não a seguir
    if is_locked:
        messages.error(request, "Esta conta é privada. Siga o usuário para ver as conexões.")
        return redirect('user_profile', username=username)
        
    connections = []
    title = ""
    
    if list_type == 'followers':
        # Busca perfis que seguem o target_user
        connections = Profile.objects.filter(following=profile).select_related('user')
        title = f"Seguidores de @{username}"
    elif list_type == 'following':
        # Busca perfis que o target_user segue
        connections = profile.following.all().select_related('user')
        title = f"Pessoas que @{username} segue"
        
    context = {
        'target_user': target_user,
        'connections': connections,
        'title': title,
    }
    return render(request, 'users/user_connections.html', context)