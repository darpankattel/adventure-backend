from django.urls import path, include

# appended with /api/

urlpatterns = [
    path('account/', include('account.urls')),
    path('campaign/', include('campaign.urls')),
    path('canvas/', include('canvas.urls')),
    path('bg/', include('background.urls')),
    path('prod/', include('productimage.urls')),
]
