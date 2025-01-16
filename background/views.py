from rest_framework import viewsets
from .models import BackgroundImage
from .serializers import BackgroundImageSerializer


class BackgroundImageViewSet(viewsets.ModelViewSet):
    queryset = BackgroundImage.objects.all()
    serializer_class = BackgroundImageSerializer

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)
