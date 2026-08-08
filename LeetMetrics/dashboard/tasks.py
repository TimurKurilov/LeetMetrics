from leetcode.views import save_leetcode_userdata, save_leetcode_usercontest, save_leetcode_user_skill_stats
from leetcode.services.snapshot import create_daily_snapshot, create_daily_skill_snapshot, generate_fake_snapshots, generate_fake_skill_snapshots
from concurrent.futures import ThreadPoolExecutor
from leetcode.models import LeetCodeUserAccount
from leetcode.views import leetcode_userdata, leetcode_usercontest, leetcode_user_skill_stats
from django.core.cache import cache
from celery import shared_task


@shared_task
def save_all_data(username, profile_data, contest_data, skill_stats):
    
    save_leetcode_userdata(username, profile_data)
    print("save_leetcode_userdata")
    
    save_leetcode_usercontest(username, contest_data)
    print("save_leetcode_usercontest")
    
    save_leetcode_user_skill_stats(username, skill_stats)
    print("save_leetcode_user_skill_stats")
    
    create_daily_snapshot(username)
    print("create_daily_snapshot")
    
    create_daily_skill_snapshot(username)
    print("create_daily_skill_snapshot")
    
    generate_fake_snapshots(username)
    print("create_daily_skill_snapshot")
    
    generate_fake_skill_snapshots(username)
    print("generate_fake_skill_snapshots")
    
    cache.delete(f"dashboard_json_{username}")
    
@shared_task
def update_all_users():
    usernames = LeetCodeUserAccount.objects.values_list("username", flat=True)

    for username in usernames:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_profile = executor.submit(leetcode_userdata, username)
            future_contest = executor.submit(leetcode_usercontest, username)
            future_skills = executor.submit(leetcode_user_skill_stats, username)

            profile_data = future_profile.result(timeout=10)
            contest_data = future_contest.result(timeout=10)
            skill_stats = future_skills.result(timeout=10)

        save_all_data.delay(username, profile_data, contest_data, skill_stats)