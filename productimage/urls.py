from .views import ProductImageViewSet
from rest_framework.routers import DefaultRouter

# appended with /api/bg
router = DefaultRouter()
router.register('', ProductImageViewSet)

urlpatterns = router.urls
