from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('new_game/', views.GameCreate.as_view(), name='new_game'),
    path('my_games/', views.user_games, name='user_games'),
    path('games/<slug:slug>/<int:pk>/edit/', views.GameEdit.as_view(),
         name='game_edit'),
    path('games/<slug:slug>/delete/', views.GameDelete.as_view(),
         name='game_delete'),
    path('games/<slug:slug>/signup/', views.game_join, name='game_join'),
    path('user/<int:pk>/preferences/', views.AddUserPrefers.as_view(),
         name='user_preferences')
]
