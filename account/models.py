from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)

    # Profile picture from Google
    picture = models.URLField(null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    website = models.URLField(null=True, blank=True,
                              help_text='Your personal website')

    def __str__(self):
        return self.user.username
