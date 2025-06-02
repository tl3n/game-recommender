# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
from recommender import Recommender
from utils import fetch_owned_games
from models import UserGamePreference, GameStatus, Game, init_db

app = FastAPI()

# Initialize database
engine = init_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize recommender with database session
db = SessionLocal()
recommender = Recommender(db)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GameStatusUpdate(BaseModel):
    status: str
    steamid: str


@app.post("/games/{appid}/status")
async def update_game_status(appid: str, status_update: GameStatusUpdate, db: Session = Depends(get_db)):
    try:
        # Validate status
        game_status = GameStatus(status_update.status.lower())
        
        # Check if game exists
        game = db.query(Game).filter(Game.appid == appid).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Check if preference already exists
        existing_pref = db.query(UserGamePreference).filter(
            UserGamePreference.steam_id == status_update.steamid,
            UserGamePreference.appid == appid
        ).first()
        
        if existing_pref:
            # Update existing preference
            existing_pref.status = game_status
        else:
            # Create new preference
            new_pref = UserGamePreference(
                steam_id=status_update.steamid,
                appid=appid,
                status=game_status
            )
            db.add(new_pref)
        
        db.commit()
        return {"message": "Game status updated successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'liked' or 'disliked'")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations")
async def get_recommendations(steam_id: str, db: Session = Depends(get_db)):
    user_games = fetch_owned_games(steam_id)
    if not user_games:
        raise HTTPException(status_code=404, detail="No games found or Steam ID invalid")
    
    # Get user preferences
    preferences = db.query(UserGamePreference).filter(
        UserGamePreference.steam_id == steam_id
    ).all()
    
    # Convert preferences to dict for easier lookup
    user_preferences = {
        pref.appid: pref.status.value 
        for pref in preferences
    }
    
    try:
        return recommender.recommend(user_games, 10, user_preferences)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    db.close()