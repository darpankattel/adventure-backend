from rest_framework import viewsets
from .models import CanvasState
from .serializers import CanvasStateSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CanvasStateViewSet(viewsets.ModelViewSet):
    queryset = CanvasState.objects.all()
    serializer_class = CanvasStateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)
