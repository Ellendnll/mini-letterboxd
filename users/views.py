from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import RegisterForm, UpdateUserForm


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