from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu email'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):

        email = self.cleaned_data.get('email')

        invalid_domains = [
            'gamil.com',
            'gmial.com',
            'hotmial.com',
            'yaho.com'
        ]

        domain = email.split('@')[-1]

        if domain in invalid_domains:

            raise ValidationError(
                'Digite um email válido.'
            )

        if User.objects.filter(email=email).exists():

            raise ValidationError(
                'Este email já está cadastrado.'
            )

        return email
    
    def clean_username(self):

        username = self.cleaned_data.get('username')

        if len(username) < 3:

             raise ValidationError(
                'O nome de usuário deve ter pelo menos 3 caracteres.'
            )

        return username


class UpdateUserForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_username(self):

        username = self.cleaned_data.get('username')

        if len(username) < 3:

            raise ValidationError(
                'O nome de usuário deve ter pelo menos 3 caracteres.'
            )

        return username
