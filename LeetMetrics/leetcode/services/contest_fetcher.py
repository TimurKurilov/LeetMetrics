import requests
from leetcode.graphql_queries.contest_queries import USER_CONTEST_QUERY

class LeetCodeContestFetcher:
    def fetch_contest(self, username):
        self.url = "https://leetcode.com/graphql"
        variables = {
            "username": username
        }
        
        response = requests.post(
            self.url,
            json={
                "query": USER_CONTEST_QUERY,
                "variables": variables
            }
        )
        
        data = response.json()
        return data