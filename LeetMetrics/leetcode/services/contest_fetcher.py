from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from leetcode.graphql_queries.contest_queries import USER_CONTEST_QUERY


class LeetCodeContestFetcher:

    def _get_cookies(self, username):
        options = Options()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://leetcode.com/{username}/")
        driver.implicitly_wait(10)
        cookies = driver.get_cookies()
        driver.quit()

        return cookies

    def _build_session(self, cookies):
        session = requests.Session()

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
            "Content-Type": "application/json"
        })

        return session

    def fetch_contest(self, username):
        url = "https://leetcode.com/graphql"

        cookies = self._get_cookies(username)
        session = self._build_session(cookies)

        variables = {"username": username}

        response = session.post(
            url,
            json={
                "query": USER_CONTEST_QUERY,
                "variables": variables
            }
        )

        return response.json()