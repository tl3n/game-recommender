import os
import httpx
import pandas as pd
import json
import requests
from dotenv import load_dotenv

load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

def fetch_owned_games(steam_id: str) -> list[dict]:
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steam_id,
        "format": "json",
        "include_appinfo": True
    }

    print(f"Fetching games for: {steam_id}")
    response = requests.get(url, params=params)
    print("Steam API Response:", response.status_code, response.text[:300])

    data = response.json()
    return data.get("response", {}).get("games", [])


def load_metadata(filepath: str = "data/steam_games_metadata.json") -> pd.DataFrame:
    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    rows = []
    for appid_str, game in raw_data.items():
        try:
            appid = int(appid_str)
            name = game.get("name", "")
            genres = game.get("genres", [])
            tags_data = game.get("tags", {})
            # Handle both dictionary and list formats for tags
            tags = list(tags_data.keys()) if isinstance(tags_data, dict) else tags_data
            description = game.get("detailed_description") or game.get("about_the_game") or game.get("short_description", "")
            positive = game.get("positive", 0)
            negative = game.get("negative", 0)
            developer = game.get("developers", [])
            publisher = game.get("publishers", [])

            rows.append({
                "appid": appid,
                "name": name,
                "genres": genres,
                "tags": tags,
                "description": description,
                "positive": positive,
                "negative": negative,
                "developer": developer,
                "publisher": publisher
            })
        except Exception as e:
            print(f"Skipping game {appid_str} due to error: {e}")
    
    df = pd.DataFrame(rows)
    df.dropna(subset=["appid", "name", "tags", "genres", "description"], inplace=True)
    return df
