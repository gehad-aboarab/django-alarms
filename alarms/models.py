from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Class that represents an alarm in the database
class Alarm(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ", " + self.user.username

    def get_absolute_url(self):
        return reverse('home')
