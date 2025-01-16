from .views import CanvasStateViewSet
from rest_framework.routers import DefaultRouter

# appended with /api/canvas/

router = DefaultRouter()
router.register(r"", CanvasStateViewSet)

urlpatterns = router.urls
