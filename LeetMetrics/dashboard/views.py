from django.shortcuts import render
from leetcode.services.snapshot import create_daily_snapshot, create_daily_skill_snapshot, generate_fake_snapshots, generate_fake_skill_snapshots
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest, leetcode_user_skill_stats, save_leetcode_user_skill_stats

def dashboard(request, username):
    profile_data = leetcode_userdata(username=username)
    contest_data = leetcode_usercontest(username=username)
    skill_stats = leetcode_user_skill_stats(username=username)

    save_leetcode_userdata(username, profile_data)
    save_leetcode_usercontest(username, contest_data)
    save_leetcode_user_skill_stats(username, skill_stats)

    create_daily_snapshot(username)
    create_daily_skill_snapshot(username)
    generate_fake_snapshots(username=username)
    generate_fake_skill_snapshots(username=username)

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