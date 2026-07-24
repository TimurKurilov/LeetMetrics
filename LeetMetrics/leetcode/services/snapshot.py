import random
from datetime import timedelta

from django.http import JsonResponse
from django.core.cache import cache
from leetcode.models import DailyStatsSnapshot, DailySkillStatsSnapshot, LeetCodeUserAccount, LeetCodeUserContestStats, LeetCodeUserSkillStat
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest
from django.utils import timezone


def create_daily_snapshot(username):
    account = LeetCodeUserAccount.objects.select_related(
        "contest_stats"
    ).get(username=username)

    contest = account.contest_stats
    today = timezone.now().date()
    
    _, created = DailyStatsSnapshot.objects.get_or_create(
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
    if created:
        cache.delete(f"dashboard_json_{username}")
    
def generate_fake_snapshots(username, days=90):
    account = LeetCodeUserAccount.objects.select_related("contest_stats").get(username=username)

    existing_count = DailyStatsSnapshot.objects.filter(account=account).count()
    if existing_count >= 90:
        return None

    last_snapshot = (
        DailyStatsSnapshot.objects.filter(account=account)
        .order_by("-date")
        .first()
    )
    if not last_snapshot:
        raise ValueError("Сначала создайте хотя бы один настоящий DailyStatsSnapshot.")

    current_date = last_snapshot.date
    ranking = last_snapshot.ranking
    reputation = last_snapshot.reputation
    easy = last_snapshot.easy
    medium = last_snapshot.medium
    hard = last_snapshot.hard

    has_contest = last_snapshot.contest_rating is not None
    contest_rating = last_snapshot.contest_rating
    global_ranking = last_snapshot.global_ranking
    attended_contests = last_snapshot.attended_contests
    total_participants = last_snapshot.total_participants
    top_percentage = last_snapshot.top_percentage

    for _ in range(days):
        current_date += timedelta(days=1)

        easy += random.randint(0, 2)
        if random.randint(0, 1) == 1:
            medium += random.randint(0, 1)
        else:
            hard += random.randint(0, 1)

        total = easy + medium + hard
        ranking -= random.randint(-3, 5)

        if has_contest:
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

def create_daily_skill_snapshot(username):
    account = LeetCodeUserAccount.objects.get(username=username)
    skill_stats = LeetCodeUserSkillStat.objects.filter(account=account)
    today = timezone.now().date()

    created_any = False
    for stat in skill_stats:
        _, created = DailySkillStatsSnapshot.objects.get_or_create(
            account=account,
            date=today,
            tag_slug=stat.tag_slug,
            level=stat.level,
            defaults={
                "tag_name": stat.tag_name,
                "problems_solved": stat.problems_solved,
            }
        )
        if created:
            created_any = True
    if created_any:
        cache.delete(f"dashboard_json_{username}")

def generate_fake_skill_snapshots(username, days=90):
    account = LeetCodeUserAccount.objects.get(username=username)

    existing_count = DailySkillStatsSnapshot.objects.filter(account=account).count()
    if existing_count >= days * 5:
        return None

    last_snapshot = (
        DailySkillStatsSnapshot.objects.filter(account=account)
        .order_by("-date")
        .first()
    )
    if not last_snapshot:
        raise ValueError("Сначала создайте хотя бы один настоящий DailySkillStatsSnapshot.")

    current_date = last_snapshot.date
    tag_data = {}

    snapshots = DailySkillStatsSnapshot.objects.filter(
        account=account, date=last_snapshot.date
    )
    for snap in snapshots:
        tag_data[snap.tag_slug] = {
            "tag_name": snap.tag_name,
            "level": snap.level,
            "problems_solved": snap.problems_solved,
        }

    for _ in range(days):
        current_date += timedelta(days=1)

        for tag_slug, info in tag_data.items():
            info["problems_solved"] += random.randint(0, 2)

            DailySkillStatsSnapshot.objects.create(
                account=account,
                date=current_date,
                tag_name=info["tag_name"],
                tag_slug=tag_slug,
                level=info["level"],
                problems_solved=info["problems_solved"],
            )
        
def dashboard_data(request, username):
    cache_key = f"dashboard_json_{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return JsonResponse(cached)

    generate_fake_snapshots(username=username)
    generate_fake_skill_snapshots(username=username)

    account = LeetCodeUserAccount.objects.get(
        username=username
    )

    snapshots = DailyStatsSnapshot.objects.filter(
        account=account
    ).order_by("date")

    skill_snapshots = DailySkillStatsSnapshot.objects.filter(
        account=account
    ).order_by("date")

    data = {
        "dates": [],
        "total": [],
        "easy": [],
        "medium": [],
        "hard": [],
        "rating": [],
        "skill_dates": [],
        "skills": {},
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

    seen_dates = set()
    for snap in skill_snapshots:
        date_str = snap.date.strftime("%Y-%m-%d")
        if date_str not in seen_dates:
            data["skill_dates"].append(date_str)
            seen_dates.add(date_str)

        key = f"{snap.tag_slug}_{snap.level}"
        if key not in data["skills"]:
            data["skills"][key] = {
                "tag_name": snap.tag_name,
                "tag_slug": snap.tag_slug,
                "level": snap.level,
                "dates": [],
                "problems_solved": [],
            }
        data["skills"][key]["dates"].append(date_str)
        data["skills"][key]["problems_solved"].append(snap.problems_solved)

    cache.set(cache_key, data, 60 * 60)
    return JsonResponse(data)