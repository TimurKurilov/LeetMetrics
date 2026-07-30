from concurrent.futures import ThreadPoolExecutor

from .tasks import save_all_data
from django.shortcuts import render
from leetcode.views import leetcode_userdata, leetcode_usercontest, leetcode_user_skill_stats

def dashboard(request, username):
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_profile = executor.submit(leetcode_userdata, username)
        future_contest = executor.submit(leetcode_usercontest, username)
        future_skills = executor.submit(leetcode_user_skill_stats, username)

        profile_data = future_profile.result(timeout=5)
        contest_data = future_contest.result(timeout=5)
        skill_stats = future_skills.result(timeout=5)

    save_all_data.delay(username, profile_data, contest_data, skill_stats)

    has_contest = contest_data.get("contest_rating") is not None

    skills_by_level = {"fundamental": [], "intermediate": [], "advanced": []}
    for skill in skill_stats:
        skills_by_level[skill["level"]].append(skill)

    return render(request, template_name="dashboard/dashboard.html", context={
        "data": profile_data,
        "contest_data": contest_data,
        "username": username,
        "has_contest": has_contest,
        "skill_stats": skill_stats,
        "skills_by_level": skills_by_level,
    })