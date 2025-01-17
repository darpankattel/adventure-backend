from rest_framework import viewsets
from .models import BackgroundImage
from .serializers import BackgroundImageSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BackgroundImageViewSet(viewsets.ModelViewSet):
    queryset = BackgroundImage.objects.all()
    serializer_class = BackgroundImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)
