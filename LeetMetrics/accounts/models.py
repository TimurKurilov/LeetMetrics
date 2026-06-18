from django.db import models
from django.contrib.auth.models import User

class LeetCodeUserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    last_sync = models.DateTimeField(null=True, blank=True)