#!/bin/bash

# Check if database exists and has games
if [ ! -f "game_recommender.db" ] || [ ! -s "game_recommender.db" ]; then
    echo "Database not found or empty. Loading games from JSON..."
    python load_games.py
else
    echo "Database exists. Checking if games are loaded..."
    # Check if games table has any entries
    if ! python -c "from models import Game, init_db; from sqlalchemy.orm import Session; from sqlalchemy.orm import sessionmaker; engine = init_db(); SessionLocal = sessionmaker(bind=engine); db = SessionLocal(); print(db.query(Game).count() > 0); db.close()"; then
        echo "No games found in database. Loading games from JSON..."
        python load_games.py
    else
        echo "Games already loaded in database."
    fi
fi

# Start the FastAPI server
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 