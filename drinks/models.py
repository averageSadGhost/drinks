from django.db import models
from django.conf import settings

class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='drink_images/', null=True, blank=True)  # New field for image upload

    def __str__(self):
        return self.name
