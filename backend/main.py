# main.py
from fastapi import FastAPI, HTTPException
from recommender import Recommender
from utils import fetch_owned_games, load_metadata

app = FastAPI()

# Initialize recommender once
metadata = load_metadata("games.json")
recommender = Recommender(metadata)

@app.get("/recommendations")
async def get_recommendations(steam_id: str):
    user_games = fetch_owned_games(steam_id)
    if not user_games:
        raise HTTPException(status_code=404, detail="No games found or Steam ID invalid")
    try:
        return recommender.recommend(user_games, 20)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
