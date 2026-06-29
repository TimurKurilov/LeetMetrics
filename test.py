import requests
import json

url = "https://leetcode.com/graphql"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

query = """
query userContestRankingInfo($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
    totalParticipants
    topPercentage
  }
"""

variables = {"username": "vetor"}

response = requests.post(
    url,
    headers=headers,
    json={
        "query": query,
        "variables": variables
    }
)

# 1. СНАЧАЛА проверяем статус
print("STATUS:", response.status_code)

# 2. Смотрим сырой ответ (это самое важное для дебага)
print("RAW RESPONSE:")
print(response.text[:500])

# 3. Пытаемся парсить JSON только если это реально JSON
try:
    data = response.json()
    print("\nPARSED JSON:")
    print(json.dumps(data, indent=4, ensure_ascii=False))
except Exception as e:
    print("\nJSON PARSE ERROR:", e)


# второй запрос
query2 = """
query userPublicProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      userAvatar
      realName
      aboutMe
      school
      websites
      countryName
      reputation
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

response2 = requests.post(
    url,
    headers=headers,
    json={
        "query": query2,
        "variables": variables
    }
)

print("\nSTATUS 2:", response2.status_code)
print("RAW RESPONSE 2:")
print(response2.text[:500])

try:
    data2 = response2.json()
    print("\nPARSED JSON 2:")
    print(json.dumps(data2, indent=4, ensure_ascii=False))
except Exception as e:
    print("\nJSON PARSE ERROR 2:", e)