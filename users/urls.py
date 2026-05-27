from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    
    path('register/', views.register_view, name='register'),
    
    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    
    
    path('profile/', views.profile_view, name='profile'),
    
    
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    
    
    path('profile/<str:username>/follow/', views.follow_toggle_view, name='follow_toggle'),

    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/change_password.html'
        ),
        name='change_password'
    ),
    
    path('search-users/', views.user_search_view, name='user_search'),
    
    path('profile/<str:username>/followers/', views.user_connections_view, {'list_type': 'followers'}, name='user_followers'),
    
    path('profile/<str:username>/following/', views.user_connections_view, {'list_type': 'following'}, name='user_following'),
]