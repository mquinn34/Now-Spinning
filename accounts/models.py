from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Profile

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


    def __str__(self):
        return self.username

