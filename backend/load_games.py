import json
import ijson  # For streaming JSON parsing
from sqlalchemy.orm import Session
from models import Game, init_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tqdm

def load_games_to_db(json_file: str = "games.json", batch_size: int = 1000):
    """Load games from JSON file into database in batches."""
    # Initialize database
    engine = init_db()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        print(f"Loading games from {json_file}...")
        batch = []
        
        # Load and parse JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            games_data = json.load(f)
            total_games = len(games_data)
            
            # Process games in batches
            for appid_str, game in tqdm.tqdm(games_data.items(), total=total_games, desc="Loading games"):
                try:
                    appid = int(appid_str)
                    
                    # Calculate review metrics
                    positive = game.get('positive', 0)
                    negative = game.get('negative', 0)
                    total_reviews = positive + negative
                    review_ratio = positive / (total_reviews + 1e-6)
                    
                    # Create Game instance
                    game_obj = Game(
                        appid=appid,
                        name=game.get('name', ''),
                        release_date=game.get('release_date', ''),
                        detailed_description=game.get('detailed_description', ''),
                        short_description=game.get('short_description', ''),
                        header_image=game.get('header_image', ''),
                        screenshots=game.get('screenshots', []),
                        genres=game.get('genres', []),
                        tags=list(game.get('tags', {}).keys()) if isinstance(game.get('tags'), dict) else game.get('tags', []),
                        positive=positive,
                        negative=negative,
                        developer=game.get('developers', []),
                        publisher=game.get('publishers', []),
                        total_reviews=total_reviews,
                        review_ratio=review_ratio,
                        popularity_score=0.0  # Will be updated after all games are loaded
                    )
                    
                    batch.append(game_obj)
                    
                    # When batch is full, commit to database
                    if len(batch) >= batch_size:
                        db.bulk_save_objects(batch)
                        db.commit()
                        batch = []
                        
                except Exception as e:
                    print(f"Error processing game {appid_str}: {e}")
                    continue
            
            # Commit any remaining games
            if batch:
                db.bulk_save_objects(batch)
                db.commit()
        
        # Update popularity scores
        print("Updating popularity scores...")
        max_reviews = db.query(Game.total_reviews).order_by(Game.total_reviews.desc()).first()[0]
        db.query(Game).update({
            Game.popularity_score: Game.total_reviews / (max_reviews + 1e-6)
        })
        db.commit()
        
        print("Games loaded successfully!")
        
    except Exception as e:
        print(f"Error loading games: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    load_games_to_db() 