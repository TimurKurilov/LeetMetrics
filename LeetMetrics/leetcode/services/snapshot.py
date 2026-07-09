import random
from datetime import timedelta

from django.http import JsonResponse
from leetcode.models import DailyStatsSnapshot, LeetCodeUserAccount, LeetCodeUserContestStats
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest
from django.utils import timezone


def create_daily_snapshot(username):
    account = LeetCodeUserAccount.objects.select_related(
        "contest_stats"
    ).get(username=username)

    contest = account.contest_stats
    today = timezone.now().date()
    
    DailyStatsSnapshot.objects.get_or_create(
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
    
def generate_fake_snapshots(username, days=90):
    account = LeetCodeUserAccount.objects.select_related(
        "contest_stats"
    ).get(username=username)

    existing_count = DailyStatsSnapshot.objects.filter(account=account).count()
    if existing_count >= 90:
        return None
    contest = account.contest_stats

    last_snapshot = (
        DailyStatsSnapshot.objects.filter(account=account)
        .order_by("-date")
        .first()
    )

    if not last_snapshot:
        raise ValueError(
            "Сначала создайте хотя бы один настоящий DailyStatsSnapshot."
        )

    current_date = last_snapshot.date

    ranking = last_snapshot.ranking
    reputation = last_snapshot.reputation

    easy = last_snapshot.easy
    medium = last_snapshot.medium
    hard = last_snapshot.hard

    contest_rating = last_snapshot.contest_rating
    global_ranking = last_snapshot.global_ranking
    attended_contests = last_snapshot.attended_contests
    total_participants = last_snapshot.total_participants
    top_percentage = last_snapshot.top_percentage

    for _ in range(days):
        current_date += timedelta(days=1)

        easy += random.randint(0, 2)
        if random.randint(0,1) == 1:
            medium += random.randint(0, 1)
        else:
            hard += random.randint(0, 1)

        total = easy + medium + hard

        ranking -= random.randint(-3, 5)
        contest_rating += random.randint(-10, 15)

        DailyStatsSnapshot.objects.create(
            account=account,
            date=current_date,

            ranking=ranking,
            reputation=reputation,

            total=total,
            easy=easy,
            medium=medium,
            hard=hard,

            contest_rating=contest_rating,
            global_ranking=global_ranking,
            attended_contests=attended_contests,
            total_participants=total_participants,
            top_percentage=top_percentage,
        )
        
def dashboard_data(request, username):
    generate_fake_snapshots(username=username)

    account = LeetCodeUserAccount.objects.get(
        username=username
    )

    snapshots = DailyStatsSnapshot.objects.filter(
        account=account
    ).order_by("date")

    data = {
        "dates": [],
        "total": [],
        "easy": [],
        "medium": [],
        "hard": [],
        "rating": [],
    }

    for snapshot in snapshots:
        data["dates"].append(
            snapshot.date.strftime("%Y-%m-%d")
        )

        data["total"].append(snapshot.total)
        data["easy"].append(snapshot.easy)
        data["medium"].append(snapshot.medium)
        data["hard"].append(snapshot.hard)
        data["rating"].append(snapshot.contest_rating)

    return JsonResponse(data)