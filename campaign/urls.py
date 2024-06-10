from django.urls import path, include
from . import views

# appended with /api/campaign/

urlpatterns = [
    path('', views.CampaignListCreateView.as_view(), name='campaign-list-create'),
    path('<str:id>/', views.CampaignRetrieveUpdateDestroyView.as_view(),
         name='campaign-retrieve-update-destroy'),

]
