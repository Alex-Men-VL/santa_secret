from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.RegisterUser.as_view(), name='signup'),
    path('accounts/login/', views.LoginUser.as_view(), name='login'),
    path('accounts/user/<int:pk>/', views.UserAccount.as_view(),
         name='account'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('accounts/user/<int:pk>/preferences/', views.AddUserPrefers.as_view(),
         name='user_preferences'),
    path('games/new_game/', views.GameCreate.as_view(), name='new_game'),
    path('games/my_games/', views.user_games, name='user_games'),
    path('games/<slug:slug>/<int:pk>/edit/', views.GameEdit.as_view(),
         name='game_edit'),
    path('games/<slug:slug>/delete/', views.GameDelete.as_view(),
         name='game_delete'),
    path('games/<slug:slug>/signup/', views.game_join, name='game_join'),
    path('games/preferences/', views.users_preferences,
         name='users_preferences'),
]
