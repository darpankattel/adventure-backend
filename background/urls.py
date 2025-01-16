from .views import BackgroundImageViewSet
from rest_framework.routers import DefaultRouter

# appended with /api/bg
router = DefaultRouter()
router.register('', BackgroundImageViewSet)

urlpatterns = router.urls
