from django.shortcuts import render
from leetcode.services.snapshot import create_daily_snapshot, generate_fake_snapshots
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest

def dashboard(request, username):
    profile_data = leetcode_userdata(username=username)
    contest_data = leetcode_usercontest(username=username)
    save_leetcode_userdata(username, profile_data)
    save_leetcode_usercontest(username, contest_data)

    create_daily_snapshot(username)
    generate_fake_snapshots(username=username)
    has_contest = contest_data.get("contest_rating") is not None
    return render(request, template_name="dashboard/dashboard.html", context={"data": profile_data, "contest_data": contest_data, "username": username, "has_contest": has_contest,})