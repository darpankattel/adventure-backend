from rest_framework import serializers
from .models import CanvasState


class CanvasStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanvasState
        fields = ["campaign", "created_at", "updated_at", "data"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
