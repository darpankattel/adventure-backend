from django.db import models
from campaign.models import Campaign


class BackgroundImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="backgrounds")
    image = models.ImageField(upload_to="backgrounds/", blank=True, null=True)
    prompt = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Background for {self.campaign.name}"
