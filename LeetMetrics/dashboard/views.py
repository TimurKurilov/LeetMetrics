from django.shortcuts import render
from leetcode.views import leetcode_userdata, leetcode_usercontest, save_leetcode_userdata, save_leetcode_usercontest

def dashboard(request, username):
    profile_data = leetcode_userdata(username=username)
    contest_data = leetcode_usercontest(username=username)
    
    save_leetcode_userdata(username, profile_data)
    save_leetcode_usercontest(username, contest_data)
    return render(request, template_name="dashboard/dashboard.html", context={"data": data, "contest_data": contest_data})