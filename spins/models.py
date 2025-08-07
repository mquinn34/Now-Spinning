from django.db import models
from django.conf import settings

class Spin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spins')
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='spins/', blank=True, null=True)
    album_cover_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.artist} – {self.album} by {self.user.username}"

