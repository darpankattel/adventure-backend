from .views import CampaignViewSet
from rest_framework.routers import DefaultRouter

# appended with /api/campaign/
router = DefaultRouter()
router.register(r'', CampaignViewSet)

urlpatterns = router.urls
