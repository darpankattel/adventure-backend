import requests
from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from .models import ProductImage
from .serializers import ProductImageSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
import os
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")


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

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        product_image = ProductImage.objects.get(id=pk)
        # real image path
        image = product_image.image.path
        image_name = product_image.image.name
        image_file = open(image, 'rb')
        if image:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': image_file},
                data={'size': 'auto'},
                headers={'X-Api-Key': REMOVE_BG_API_KEY},
            )
            if response.status_code == requests.codes.ok:
                with open(f'{image_name}-no-bg.png', 'wb') as out:
                    out.write(response.content)
                return response.Response({'message': 'Background removed successfully'}, status=status.HTTP_200_OK)
            else:
                print("Error:", response.status_code, response.text)

        return response.Response({'message': 'Some error occured'}, status=status.HTTP_404_NOT_FOUND)
