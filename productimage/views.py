from rest_framework import viewsets, response, status
from .models import ProductImage
from .serializers import ProductImageSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)

    # create(), retrieve(), update(), partial_update(), destroy() and list()
    def create(self, request, *args, **kwargs):
        # TODO: we will initiate a Deep Learning model here, to create the product image from the prompt
        # for now we will set image to null
        serilaizer = self.get_serializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return response.Response(serilaizer.data, status=status.HTTP_201_CREATED)
        return response.Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
