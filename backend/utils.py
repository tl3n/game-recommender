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
    response = requests.get(url, params=params)
    try:
        data = response.json()
    except Exception as e:
        print("Failed to decode JSON from Steam API. Response text:")
        print(response.text)
        raise
    return data.get("response", {}).get("games", [])


def load_metadata(filepath: str = "games.json") -> pd.DataFrame:
    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print("Loading metadata from", filepath)

    rows = []
    for appid_str, game in raw_data.items():
        try:
            appid = int(appid_str)
            name = game.get("name", "")
            print("Parsing game", name)
            release_date = game.get("release_date", [])
            detailed_description = game.get("detailed_description")
            short_description = game.get("short_description")
            genres = game.get("genres", [])
            tags_data = game.get("tags", {})
            tags = list(tags_data.keys()) if isinstance(tags_data, dict) else tags_data
            positive = game.get("positive", 0)
            negative = game.get("negative", 0)
            developer = game.get("developers", [])
            publisher = game.get("publishers", [])
            header_image = game.get("header_image", "")
            screenshots = game.get("screenshots", [])

            rows.append({
                "appid": appid,
                "name": name,
                "release_date": release_date,
                "detailed_description": detailed_description,
                "short_description": short_description,
                "header_image": header_image,
                "screenshots": screenshots,
                "genres": genres,
                "tags": tags,
                "positive": positive,
                "negative": negative,
                "developer": developer,
                "publisher": publisher
            })
        except Exception as e:
            print(f"Skipping game {appid_str} due to error: {e}")
    
    df = pd.DataFrame(rows)
    return df