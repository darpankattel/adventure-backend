from django.urls import path
from . import views

# appended with /api/account/

urlpatterns = [
    path('google/', views.GoogleAuthView.as_view(), name='google-auth'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('logout-all/', views.UserLogoutAllView.as_view(), name='logout-all'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('hardcoded-login/', views.HardcodedLoginView.as_view(),
         name='hardcoded-login'),
]
