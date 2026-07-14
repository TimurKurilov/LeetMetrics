import requests
from leetcode.graphql_queries.problemset_queries import SKILL_STATS_QUERY, PROBLEMSET_QUESTION_LIST_BY_TAG_QUERY

class LeetCodeSkillStatsFetcher:
    def __init__(self):
        self.url = "https://leetcode.com/graphql"

    def fetch_skill_stats(self, username):
        variables = {
            "username": username
        }

        response = requests.post(
            self.url,
            json={
                "query": SKILL_STATS_QUERY,
                "variables": variables
            }
        )

        data = response.json()
        return data

    def fetch_problems_by_tag(self, tag_slug, status="AC", limit=100, skip=0, category_slug=""):
        variables = {
            "categorySlug": category_slug,
            "skip": skip,
            "limit": limit,
            "filters": {
                "tags": [tag_slug],
                "status": status
            }
        }

        response = requests.post(
            self.url,
            json={
                "query": PROBLEMSET_QUESTION_LIST_BY_TAG_QUERY,
                "variables": variables
            }
        )

        data = response.json()
        return data

    def fetch_problems_by_tag_authed(self, tag_slug, session_cookie, csrf_token,
                                      status="AC", limit=100, skip=0, category_slug=""):
        variables = {
            "categorySlug": category_slug,
            "skip": skip,
            "limit": limit,
            "filters": {
                "tags": [tag_slug],
                "status": status
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
            "x-csrftoken": csrf_token,
            "Referer": "https://leetcode.com/problemset/all/",
        }

        response = requests.post(
            self.url,
            headers=headers,
            json={
                "query": PROBLEMSET_QUESTION_LIST_BY_TAG_QUERY,
                "variables": variables
            }
        )

        data = response.json()
        return data
fetcher = LeetCodeSkillStatsFetcher()
result = fetcher.fetch_skill_stats("vetor")
print(result)