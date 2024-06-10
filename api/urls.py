from django.urls import path, include

urlpatterns = [
    path('account/', include('account.urls')),
    path('campaign/', include('campaign.urls')),
    path('canvas/', include('canvas.urls')),
]
