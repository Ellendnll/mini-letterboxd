from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
     Vincula o Perfil diretamente a um Usuário do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
     Novos campos para a Biografia e Localização (podem começar vazios)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Descrição")
    location = models.CharField(max_length=100, blank=True, verbose_name="Localização")

    def __str__(self):
        return f"Perfil de {self.user.username}"

 🪄 Sinais para criar e salvar o Perfil automaticamente quando um Usuário for criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()