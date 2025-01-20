from rest_framework import serializers
from .models import BackgroundImage
from campaign.models import Campaign


class BackgroundImageSerializer(serializers.ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(
        queryset=Campaign.objects.all(), required=False
    )

    class Meta:
        model = BackgroundImage
        fields = ["id", "campaign", "image", "prompt", "created_at"]

        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "image": {"read_only": True},
        }
