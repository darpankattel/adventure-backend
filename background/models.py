from django.db import models
from campaign.models import Campaign


class BackgroundImage(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="backgrounds")
    image = models.ImageField(upload_to="backgrounds/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Background for {self.campaign.name}"
