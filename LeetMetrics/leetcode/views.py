from django.shortcuts import render
from django.core.cache import cache
from leetcode.services.profile_fetcher import LeetCodeProfileFetcher
from leetcode.services.contest_fetcher import LeetCodeContestFetcher
from leetcode.services.problemset_fetcher import LeetCodeSkillStatsFetcher
from leetcode.models import LeetCodeUserAccount, LeetCodeUserContestStats, LeetCodeUserSkillStat

def leetcode_userdata(username):
    cache_key = f"leetcode_profile_{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

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
    cache.set(cache_key, data, 60 * 30)
    return data

def leetcode_usercontest(username):
    cache_key = f"leetcode_contest_{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    fetcher = LeetCodeContestFetcher()
    raw_data = fetcher.fetch_contest(username)
    matched = raw_data["data"]["userContestRanking"]
    if not matched:
        contest_data = {
            "attended_contests": None,
            "contest_rating": None,
            "global_ranking": None,
            "total_participants": None,
            "top_percentage": None,
        }
    else:
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
    cache.set(cache_key, contest_data, 60 * 30)
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

def leetcode_user_skill_stats(username):
    cache_key = f"leetcode_skill_stats_{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    fetcher = LeetCodeSkillStatsFetcher()
    raw_data = fetcher.fetch_skill_stats(username)

    matched = raw_data["data"]["matchedUser"]
    tag_counts = matched["tagProblemCounts"]

    skills = []
    for level, tag_list in tag_counts.items():
        for tag in tag_list:
            skills.append({
                "level": level,
                "tag_name": tag["tagName"],
                "tag_slug": tag["tagSlug"],
                "problems_solved": tag["problemsSolved"],
            })
    cache.set(cache_key, skills, 60 * 30)
    return skills

def save_leetcode_user_skill_stats(username, skills_data):
    account = LeetCodeUserAccount.objects.get(username=username)
    saved = []
    for skill in skills_data:
        obj, created = LeetCodeUserSkillStat.objects.update_or_create(
            account=account,
            tag_slug=skill["tag_slug"],
            level=skill["level"],
            defaults={
                "tag_name": skill["tag_name"],
                "problems_solved": skill["problems_solved"],
            }
        )
        saved.append(obj)
    return saved