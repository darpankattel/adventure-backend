from rest_framework import serializers
from .models import CanvasState


class CanvasStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanvasState
        fields = "__all__"
