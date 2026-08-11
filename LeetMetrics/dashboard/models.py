from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from leetcode.models import LeetCodeUserAccount

class SyncJob(models.Model):
    class SyncStatus(models.TextChoices):
        NOT_START = 'not_start', _('Not Started')
        RUNNING   = 'running',   _('Running')
        FAILED = "failed", _("Failed")
        FINISHED  = 'finished',  _('Finished')
    
    account = models.OneToOneField(
                LeetCodeUserAccount,
                on_delete=models.CASCADE,
                related_name="sync_jobs"
            )
    status = models.CharField(max_length=20, choices=SyncStatus.choices, default=SyncStatus.NOT_START, db_index=True,)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    seconds_running = models.IntegerField(default=0)
    error = models.TextField(null=True, blank=True)