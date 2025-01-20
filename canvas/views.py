from django.db.models import Q
from .models import CanvasState
from rest_framework import viewsets, status, response
from .serializers import CanvasStateSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from campaign.models import Campaign


class CanvasStateViewSet(viewsets.ModelViewSet):
    queryset = CanvasState.objects.all()
    serializer_class = CanvasStateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(campaign__user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        # change the queryset to filter by campaign id
        self.queryset = self.queryset.filter(
            Q(campaign__user=self.request.user) & Q(campaign_id=kwargs['pk']))
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        campaign_id = request.data.get('campaign')
        if Campaign.objects.filter(id=campaign_id, user=request.user).exists():
            return super().create(request, *args, **kwargs)
        return response.Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            Q(campaign__user=self.request.user) & Q(campaign_id=kwargs['pk']))
        instance = queryset.first()
        serializer = self.get_serializer(
            instance, data={**request.data, "campaign": kwargs['pk']}, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            Q(campaign__user=self.request.user) & Q(campaign_id=kwargs['pk']))
        if queryset.exists():
            queryset.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
