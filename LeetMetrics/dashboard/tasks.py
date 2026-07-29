from leetcode.views import save_leetcode_userdata, save_leetcode_usercontest, save_leetcode_user_skill_stats
from leetcode.services.snapshot import create_daily_snapshot, create_daily_skill_snapshot, generate_fake_snapshots, generate_fake_skill_snapshots

from celery import shared_task


@shared_task
def save_all_data(username, profile_data, contest_data, skill_stats):
    save_leetcode_userdata(username, profile_data)
    save_leetcode_usercontest(username, contest_data)
    save_leetcode_user_skill_stats(username, skill_stats)
    
    create_daily_snapshot(username)
    create_daily_skill_snapshot(username)
    generate_fake_snapshots(username)
    generate_fake_skill_snapshots(username)