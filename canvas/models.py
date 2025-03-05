from django.db import models
from campaign.models import Campaign


def get_default_canvas_state():
    return {"elements": [], "appState": []}


class CanvasState(models.Model):
    campaign = models.OneToOneField(
        Campaign, on_delete=models.CASCADE, related_name="canvas_state")
    # Stores the entire canvas state as JSON
    data = models.JSONField(default=get_default_canvas_state)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Canvas State for {self.campaign.name} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']
