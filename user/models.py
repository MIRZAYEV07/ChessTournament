from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    rating = models.IntegerField(default=1200)
    country = models.CharField(max_length=100)
    points = models.IntegerField(default=0)  # Add points field

    def __str__(self):
        return self.name