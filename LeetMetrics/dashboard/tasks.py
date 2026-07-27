from leetcode.views import save_leetcode_userdata, save_leetcode_usercontest, save_leetcode_user_skill_stats

from celery import shared_task


@shared_task
def save_all_data(username, profile_data, contest_data, skill_stats):
    save_leetcode_userdata(username, profile_data)
    save_leetcode_usercontest(username, contest_data)
    save_leetcode_user_skill_stats(username, skill_stats)