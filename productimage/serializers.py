from rest_framework import serializers
from .models import ProductImage
from campaign.models import Campaign


class ProductImageSerializer(serializers.ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(
        queryset=Campaign.objects.all(), required=False
    )

    class Meta:
        model = ProductImage
        fields = ["id", "campaign", "image", "prompt", "created_at"]

        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "image": {"read_only": True},
        }
