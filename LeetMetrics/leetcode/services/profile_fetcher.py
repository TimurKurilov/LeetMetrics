import requests
from leetcode.graphql_queries.profile_queries import USER_PROFILE_QUERY

class LeetCodeProfileFetcher:
    def fetch_profile(self, username):
        self.url = "https://leetcode.com/graphql"
        variables = {
            "username": username
        }
        
        response = requests.post(
            self.url,
            json={
                "query": USER_PROFILE_QUERY,
                "variables": variables
            }
        )
        
        data = response.json()
        return data