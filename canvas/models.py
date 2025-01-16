from django.db import models
from campaign.models import Campaign


class CanvasState(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="canvas_states")
    data = models.JSONField()  # Stores the entire canvas state as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Canvas State for {self.campaign.name} at {self.created_at}"
