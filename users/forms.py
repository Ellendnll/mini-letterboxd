from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class RegisterForm(forms.ModelForm):

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

    password = forms.CharField(
        label="Senha",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
            'type': 'password' # Garante que comece como bolinhas
        })
    )

    password_confirm = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha',
            # Deixamos esse aqui padrão para você ver a diferença
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        invalid_domains = ['gamil.com', 'gmial.com', 'hotmial.com', 'yaho.com']
        domain = email.split('@')[-1]

        if domain in invalid_domains:
            raise ValidationError('Digite um email válido.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado.')

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
             raise ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem. Digite novamente.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


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
        
    #  Validação de segurança: Evita roubar o username de outro usuário ativo
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if len(username) < 3:
            raise ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
            
        # Verifica se o username já existe em OUTRO usuário (ignorando o atual)
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
            
        return username

    # Validação de e-mail na edição
    def clean_email(self):
        email = self.cleaned_data.get('email')
        invalid_domains = ['gamil.com', 'gmial.com', 'hotmial.com', 'yaho.com']
        domain = email.split('@')[-1]

        if domain in invalid_domains:
            raise ValidationError('Digite um email válido.')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este email já está cadastrado por outro usuário.')

        return email
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Conte um pouco sobre você e seus gostos cinematográficos...',
                'class': 'form-control' # Deixa pronto para o Integrante 4 estilizar com Bootstrap
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Ex: São Paulo, Brasil',
                'class': 'form-control'
            }),
        }