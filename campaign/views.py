from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from background.serializers import BackgroundImageSerializer
from productimage.serializers import ProductImageSerializer
from canvas.models import CanvasState


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        returned = super().create(request, *args, **kwargs)
        canvas = CanvasState.objects.create(
            campaign=Campaign.objects.get(id=returned.data['id']))
        return returned

    def update(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def bgs(self, request, pk=None):
        campaign = self.get_object()
        if campaign.user != request.user:
            return Response({'error': 'You are not allowed to view this campaign'}, status=403)

        serializer = BackgroundImageSerializer(
            campaign.backgrounds.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def prods(self, request, pk=None):
        campaign = self.get_object()
        if campaign.user != request.user:
            return Response({'error': 'You are not allowed to view this campaign'}, status=403)
        serializer = ProductImageSerializer(
            campaign.product_images.all(), many=True)
        return Response(serializer.data)
