from django.urls import path, include
from . import views

# appended with /api/account/

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/picture/', views.ProfilePictureView.as_view(),
         name='profile-picture'),

    path('password-reset/', views.PasswordResetView.as_view(), name='password-reset'),

]
