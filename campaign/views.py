from rest_framework import viewsets
from .models import Campaign
from .serializers import CampaignSerializer
from account.auth import CookieTokenAuthentication as TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
