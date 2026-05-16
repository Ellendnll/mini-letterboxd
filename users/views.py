from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm


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

    return render(request, 'users/register.html', {
        'form': form
    })


@login_required
def profile_view(request):

    return render(request, 'users/profile.html')

def home_view(request):

    return render(request, 'users/home.html')