from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import RegisterForm, UpdateUserForm

from django.contrib.auth import authenticate, login, logout


def home_view(request):

    return render(request, 'users/home.html')


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Conta criada com sucesso!'
            )

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form
        }
    )


@login_required
def profile_view(request):

    return render(
        request,
        'users/profile.html'
    )


@login_required
def edit_profile_view(request):

    if request.method == 'POST':

        form = UpdateUserForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Perfil atualizado com sucesso!'
            )

            return redirect('profile')

    else:

        form = UpdateUserForm(
            instance=request.user
        )

    return render(
        request,
        'users/edit_profile.html',
        {
            'form': form
        }
    )

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                 request,
                 'Login realizado com sucesso!'
            )

            remember_me = request.POST.get('remember_me')

            if not remember_me:
                request.session.set_expiry(0)

            return redirect('profile')

        else:

            messages.error(
                request,
                'Usuário ou senha inválidos.'
            )

    return render(
        request,
        'users/login.html'
    )

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        'Logout realizado com sucesso!'
    )

    return redirect('login')