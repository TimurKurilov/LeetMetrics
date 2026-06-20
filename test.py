import json

import requests

url = "https://leetcode.com/graphql"

query = """
query userPublicProfile($username: String!) {
  matchedUser(username: $username) {
    contestBadge {
      name
      expired
      hoverText
      icon
    }
    username
    githubUrl
    twitterUrl
    linkedinUrl
    profile {
      ranking
      userAvatar
      realName
      aboutMe
      school
      websites
      countryName
      company
      jobTitle
      skillTags
      postViewCount
      postViewCountDiff
      reputation
      reputationDiff
      solutionCount
      solutionCountDiff
      categoryDiscussCount
      categoryDiscussCountDiff
    }
  }
}
"""

variables = {"username": "hostlessbtw"}

response = requests.post(
    url,
    json={
        "query": query,
        "variables": variables
    }
)

data = response.json()

#print(print(json.dumps(data, indent=4, ensure_ascii=False)))

user = data["data"]["matchedUser"]
username = user["username"]
