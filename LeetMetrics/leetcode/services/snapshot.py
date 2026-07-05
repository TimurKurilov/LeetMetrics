from leetcode.models import DailyStatsSnapshot, LeetCodeUserAccount, LeetCodeUserContestStats
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest
from django.utils import timezone


def create_daily_snapshot(username):
    account = LeetCodeUserAccount.objects.select_related(
        "contest_stats"
    ).get(username=username)

    contest = account.contest_stats
    today = timezone.now().date()
    
    DailyStatsSnapshot.objects.update_or_create(
        account=account,
        date=today,
        defaults={
            "ranking": account.ranking,
            "reputation": account.reputation,
            "total": account.total,
            "easy": account.easy,
            "medium": account.medium,
            "hard": account.hard,
            
            "contest_rating": contest.contest_rating if contest else None,
            "global_ranking": contest.global_ranking if contest else None,
            "attended_contests": contest.attended_contests if contest else 0,
            "total_participants": contest.total_participants if contest else 0,
            "top_percentage": contest.top_percentage if contest else None,
        }
    )