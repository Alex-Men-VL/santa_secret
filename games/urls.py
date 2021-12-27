from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.RegisterUser.as_view(), name='signup'),
    path('accounts/login/', views.LoginUser.as_view(), name='login'),
    path('accounts/edit/', views.UserAccount.as_view(),
         name='account'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('accounts/user/preferences/', views.AddUserPrefers.as_view(),
         name='user_preferences'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/reset_password.html'
         ),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_sent.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_complete'),
    path('games/new_game/', views.GameCreate.as_view(), name='new_game'),
    path('games/my_games/', views.UserGames.as_view(), name='user_games'),
    path('games/<slug:slug>/edit/', views.GameEdit.as_view(),
         name='game_edit'),
    path('games/<slug:slug>/delete/', views.GameDelete.as_view(),
         name='game_delete'),
    path('games/<slug:slug>/signup/', views.game_join, name='game_join'),
    path('games/preferences/', views.UsersPreferences.as_view(),
         name='preferences'),
]
