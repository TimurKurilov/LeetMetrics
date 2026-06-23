from django.db import models
from django.contrib.auth.models import User

from django.conf.global_settings import AUTH_USER_MODEL

class LeetCodeUserAccount(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='accounts_leetcode_accounts'
    )
    username = models.CharField(max_length=50, unique=True)
    last_sync = models.DateTimeField(null=True, blank=True)