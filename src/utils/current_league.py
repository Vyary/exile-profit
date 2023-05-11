import requests


class League:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
        }
        self.leagues_api = "https://www.pathofexile.com/api/trade/data/leagues"

    def current_league(self) -> str:
        try:
            leagues_api_response = requests.get(
                self.leagues_api, headers=self.headers
            ).json()
        except requests.exceptions.RequestException as e:
            return f"Error: , {e}"

        try:
            return leagues_api_response["result"][0]["id"]
        except KeyError:
            return "Error: Unable to retrieve the current league."
