# Game Recommender - Personalized Video Game Recommender Web Application

This project is a full-stack web application designed to provide users with personalized video game recommendations. It leverages machine learning techniques to analyze a user's gaming history (obtained via the Steam API) and their explicit in-app preferences to suggest new games they might enjoy.

## Running with Docker

### Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Download the Steam Games Dataset:
   * Visit [Steam Games Dataset on Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)
   * Download the dataset
   * Extract the contents into the `backend` directory
   * Ensure the JSON file is named `games.json`

### Running the Application

1. Clone this repository:
   ```bash
   git clone https://github.com/tl3n/game-recommender.git
   cd game-recommender
   ```

2. Copy the environment example files:
   ```bash
   # For backend
   cp backend/.env.example backend/.env
   
   # For frontend
   cp frontend/.env.example frontend/.env
   ```

3. Edit the `.env` files and fill in your actual values:
   - For the backend, you'll need to set up your Steam API key
   - For the frontend, you'll need to set up your NextAuth secret and Steam API key
   - You can get your Steam API key [here](https://steamcommunity.com/dev/apikey)

4. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

5. Wait until both frontend and backend services will be up. The application will be available at:
   * Frontend: http://localhost:3000
   * Backend API: http://localhost:8000

### Development Notes

* The backend container will automatically run the database initialization script (`load_games_to_db.py`) on first startup

## Features

*   **Steam Authentication:** Users can log in securely using their Steam accounts.
*   **Personalized Recommendations:** Generates a tailored list of game recommendations based on:
    *   User's owned games and playtime on Steam.
    *   Explicit user feedback (likes/dislikes) within the application.
    *   Content-based filtering (analyzing game descriptions, genres, tags, developers, publishers).
    *   Game popularity and review scores.
    *   Diversity to avoid recommending too many games from the same developer.
*   **Interactive Discovery Queue:** Users can browse through their recommended games one by one.
*   **Detailed Game Information:** Displays comprehensive details for each recommended game, including:
    *   Name, description (short and detailed).
    *   Header image and screenshots (carousel).
    *   Release date, developer, publisher.
    *   Popular user-defined tags.
    *   Calculated recommendation score.
*   **User Feedback System:** Allows users to "Like" or "Dislike" games in their queue, which dynamically influences future recommendations.
*   **Responsive User Interface:** Built with Next.js and Tailwind CSS for a modern and responsive experience across devices.

## How it Works

1.  **Authentication:** The user logs in via their Steam account using NextAuth.js. Their Steam ID is captured.
2.  **Initial Data Fetch:**
    *   The backend's `load_games_to_db.py` script is run once to populate the SQLite database with game metadata from a JSON dataset. It calculates review ratios and initial popularity scores.
3.  **Recommendation Request:**
    *   The frontend requests recommendations from the backend, sending the user's Steam ID.
    *   The backend (`main.py`) fetches the user's owned games and playtime from the Steam Web API (`utils.py`).
    *   It also retrieves any explicit likes/dislikes for games the user has rated within the app from the `UserGamePreference` table.
4.  **Recommendation Generation (`recommender.py`):**
    *   A `Recommender` instance is initialized with all game data from the database.
    *   Textual features (description, tags, genres) are vectorized using `TfidfVectorizer`.
    *   Categorical features (developer, publisher) are encoded using `OneHotEncoder`.
    *   A target variable (`y_train`) is created based on the user's normalized playtime for their owned games, adjusted by their explicit likes (playtime \* 2.0) or dislikes (playtime \* 0.05).
    *   A `Ridge` regression model is dynamically trained on the features of the user's games and their corresponding target scores.
    *   The trained model predicts "content scores" for all games the user hasn't interacted with.
    *   The final recommendation score for each candidate game is calculated as a weighted sum of:
        *   Content score (from the Ridge model).
        *   Game's review ratio.
        *   Game's popularity score.
        *   A diversity penalty (to reduce recommendations from developers whose games the user already owns or dislikes).
        *   A preference boost for games with genres similar to those the user has explicitly liked (using Jaccard similarity).
    *   Scores are normalized to a 1-100 range.
5.  **Displaying Recommendations:** The top N recommended games are sent back to the frontend and displayed in an interactive queue.
6.  **User Feedback:** When a user likes or dislikes a game in the queue:
    *   The frontend sends this preference to a Next.js API route (`/api/games/status`).
    *   This route proxies the request to the backend's `/game-status` endpoint.
    *   The backend updates or creates an entry in the `UserGamePreference` table in the SQLite database.
7.  **Queue Completion & Revalidation:** When the user finishes the queue:
    *   The frontend triggers a revalidation of the `/recommendations` page data via a Next.js API route (`/api/revalidate`).
    *   This ensures that the next time the user visits the recommendations page, a fresh set of recommendations is fetched, taking into account their latest feedback.

## Future Improvements

*   **Incorporate Collaborative Filtering:** Implement user-based or item-based collaborative filtering, or a hybrid approach, to potentially improve recommendations, especially for users with sparse interaction data.
*   **Scalability:**
    *   Migrate from SQLite to a more robust database system like PostgreSQL for better concurrency and performance with larger datasets.
    *   Optimize recommendation algorithms for larger user bases and item catalogs.
*   **Enhanced User Profile:** Allow users to manually add favorite genres, tags, or developers to further refine their profile.
*   **More Granular Feedback:** Implement a rating system (e.g., 1-5 stars) instead of just like/dislike.
*   **"Cold Start" Problem:** Improve strategies for new users with no game history or preferences.
*   **UI/UX Enhancements:** Add filtering, sorting options for recommendations, and more visual cues.