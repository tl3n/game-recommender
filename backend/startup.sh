#!/bin/bash

# Check if database exists and has games
python load_games.py

# Start the FastAPI server
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 