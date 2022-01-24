from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_game/', views.GameCreate.as_view(), name='new'),
    path('my_games/', views.UserGames.as_view(), name='user_games'),
    path('my_preferences/', views.AddUserPrefers.as_view(), name='user_preferences'),
    path('<slug:slug>/edit/', views.GameEdit.as_view(),
         name='edit'),
    path('<slug:slug>/delete/', views.GameDelete.as_view(),
         name='delete'),
    path('<slug:slug>/signup/', views.game_join, name='join'),
    path('games/preferences/', views.UsersPreferences.as_view(),
         name='preferences'),
]
