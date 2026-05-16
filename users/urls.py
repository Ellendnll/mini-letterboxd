from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home_view, name='home'),

    path('register/', views.register_view, name='register'),

    path(
     'login/',
     views.login_view,
     name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path('profile/', views.profile_view, name='profile'),

    path(
     'edit-profile/',
     views.edit_profile_view,
     name='edit_profile'
    ),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
             template_name='users/change_password.html'
        ),
         name='change_password'
    ),
]