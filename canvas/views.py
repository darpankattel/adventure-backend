from rest_framework import viewsets
from .models import CanvasState
from .serializers import CanvasStateSerializer


class CanvasStateViewSet(viewsets.ModelViewSet):
    queryset = CanvasState.objects.all()
    serializer_class = CanvasStateSerializer

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)
