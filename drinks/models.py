from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('user', 'drink')

    def save(self, *args, **kwargs):
        if Vote.objects.filter(user=self.user, drink=self.drink).exists():
            # If the user has already voted on this drink, delete the previous vote
            Vote.objects.filter(user=self.user, drink=self.drink).delete()
        
        super().save(*args, **kwargs)

class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='drink_images/', null=True, blank=True)  # New field for image upload
    vote_count = models.IntegerField(default=0)  # New field for storing total vote count

    def __str__(self):
        return self.name
