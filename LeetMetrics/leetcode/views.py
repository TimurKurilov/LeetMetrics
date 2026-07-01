from django.shortcuts import render
from leetcode.services.profile_fetcher import LeetCodeProfileFetcher
from leetcode.services.contest_fetcher import LeetCodeContestFetcher
from leetcode.models import LeetCodeUserAccount, LeetCodeUserContestStats

def leetcode_userdata(username):
    fetcher = LeetCodeProfileFetcher()
    raw_data = fetcher.fetch_profile(username)
    
    matched = raw_data["data"]["matchedUser"]
    submitstats = matched["submitStats"]
    
    profile = matched["profile"]
    submission = submitstats["acSubmissionNum"]
    
    real_name = profile["realName"]
    avatar = profile["userAvatar"]
    ranking = profile["ranking"]
    reputation = profile["reputation"]
    
    counts = {item["difficulty"]: item["count"] for item in submission}
    
    easy = counts.get("Easy", 0)
    medium = counts.get("Medium", 0)
    hard = counts.get("Hard", 0)
    total = counts.get("All", 0)
    
    data = {
        "real_name": real_name,
        "ranking": ranking,
        "reputation": reputation,
        "avatar": avatar,
        
        "submission": {
            "easy": easy,
            "medium": medium,
            "hard": hard,
            "total": total,
        }
    }
    return data

def leetcode_usercontest(username):
    fetcher = LeetCodeContestFetcher()
    raw_data = fetcher.fetch_contest(username)
    matched = raw_data["data"]["userContestRanking"]
    attendedcount = matched["attendedContestsCount"]
    rating = matched["rating"]
    global_ranking = matched["globalRanking"]
    totalparticipants = matched["totalParticipants"]
    toppercentage = matched["topPercentage"]
    
    contest_data = {
        "attended_contests": attendedcount,
        "contest_rating": rating,
        "global_ranking": global_ranking,
        "total_participants": totalparticipants,
        "top_percentage": toppercentage,
    }
    return contest_data

def save_leetcode_userdata(username, data):
    local_data = data.copy()
    submission_data = local_data.pop("submission")
    save_data, created = LeetCodeUserAccount.objects.update_or_create(username=username, defaults={**local_data, **submission_data})
    return save_data

def save_leetcode_usercontest(username, data):
    account = LeetCodeUserAccount.objects.get(username=username)
    local_data = data.copy()
    save_data, created = LeetCodeUserContestStats.objects.update_or_create(account=account, defaults={**local_data})
    return save_data