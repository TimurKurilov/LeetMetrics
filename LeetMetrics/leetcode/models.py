from django.db import models
from django.contrib.auth.models import User

class LeetCodeUserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    real_name = models.CharField(max_length=100, blank=True)
    ranking = models.IntegerField(max_length=8, unique=False)
    reputation = models.IntegerField(default=0, unique=False, default=0)
    
    total_solved = models.IntegerField()
    easy_solved = models.IntegerField()
    medium_solved = models.IntegerField()
    hard_solved = models.IntegerField()
    
    contest_rating = models.FloatField(null=True, blank=True)
    contest_global_ranking = models.IntegerField(null=True, blank=True)
    attended_contests = models.IntegerField(default=0)
    top_percentage = models.FloatField(null=True, blank=True)

    
    avatar_url = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    last_synced_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username