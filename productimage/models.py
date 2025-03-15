from django.db import models
from campaign.models import Campaign


class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(
        upload_to="product_images/", blank=True, null=True)
    prompt = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product Image for {self.campaign.name}"

    class Meta:
        ordering = ["-created_at"]
