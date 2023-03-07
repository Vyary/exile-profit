import requests


def current_league() -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json",
    }
    leagues_api = "https://www.pathofexile.com/api/trade/data/leagues"

    try:
        leagues_api_response = requests.get(leagues_api, headers=headers).json()
    except requests.exceptions.RequestException as e:
        return f"Error: , {e}"

    try:
        return leagues_api_response["result"][0]["id"]
    except KeyError:
        return "Error: Unable to retrieve the current league."
