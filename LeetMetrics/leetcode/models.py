from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LeetCodeUserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    real_name = models.CharField(default=None,max_length=100, blank=True)
    ranking = models.IntegerField(unique=False)
    reputation = models.IntegerField(default=0, unique=False)
    
    total= models.IntegerField()
    easy = models.IntegerField()
    medium = models.IntegerField()
    hard = models.IntegerField()

    
    avatar = models.URLField(blank=True)
    #country = models.CharField(default=None, max_length=100, blank=True)
    last_synced_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
class LeetCodeUserContestStats(models.Model):
    account = models.OneToOneField(
        LeetCodeUserAccount,
        on_delete=models.CASCADE,
        related_name="contest_stats"
    )
    
    contest_rating = models.FloatField(default=None, null=True, blank=True)
    global_ranking = models.IntegerField(default=None, null=True, blank=True)
    attended_contests = models.IntegerField(default=0, null=True)
    total_participants = models.IntegerField(default=0, null=True)
    top_percentage = models.FloatField(default=None, null=True, blank=True)
    
    
class LeetCodeUserSkillStat(models.Model):
    class SkillLevel(models.TextChoices):
        FUNDAMENTAL = "fundamental", "Fundamental"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    account = models.ForeignKey(
        LeetCodeUserAccount,
        on_delete=models.CASCADE,
        related_name="skill_stats"
    )

    level = models.CharField(max_length=20, choices=SkillLevel.choices)
    tag_name = models.CharField(max_length=100)
    tag_slug = models.CharField(max_length=100)
    problems_solved = models.IntegerField(default=0)

    last_synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["level", "-problems_solved"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "tag_slug", "level"],
                name="unique_account_tag_level"
            )
        ]

    def __str__(self):
        return f"{self.account.username} - {self.tag_name} ({self.level}): {self.problems_solved}"

class DailySkillStatsSnapshot(models.Model):
    account = models.ForeignKey(
        LeetCodeUserAccount,
        on_delete=models.CASCADE,
        related_name="daily_skill_snapshots"
    )

    date = models.DateField(default=timezone.now)

    level = models.CharField(max_length=20, choices=LeetCodeUserSkillStat.SkillLevel.choices)
    tag_name = models.CharField(max_length=100)
    tag_slug = models.CharField(max_length=100)
    problems_solved = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "date", "tag_slug", "level"],
                name="unique_daily_skill_snapshot"
            )
        ]

    def __str__(self):
        return f"{self.account.username} - {self.tag_name} - {self.date}"

class DailyStatsSnapshot(models.Model):
    account = models.ForeignKey(
        LeetCodeUserAccount,
        on_delete=models.CASCADE,
        related_name="daily_snapshots"
    )

    date = models.DateField(default=timezone.now)

    ranking = models.IntegerField()
    reputation = models.IntegerField()

    total = models.IntegerField()
    easy = models.IntegerField()
    medium = models.IntegerField()
    hard = models.IntegerField()

    contest_rating = models.FloatField(null=True, blank=True)
    global_ranking = models.IntegerField(null=True, blank=True)
    attended_contests = models.IntegerField(default=0, null=True)
    total_participants = models.IntegerField(default=0, null=True)
    top_percentage = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["account", "date"],
                name="unique_daily_snapshot"
            )
        ]

    def __str__(self):
        return f"{self.account.username} - {self.date}"