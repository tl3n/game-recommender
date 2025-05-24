# recommender.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.preprocessing import OneHotEncoder
from sqlalchemy.orm import Session
from models import Game
from typing import List, Dict, Any
import pandas as pd

class Recommender:
    def __init__(self, db: Session, min_reviews: int = 100, review_weight: float = 0.3, 
                 popularity_weight: float = 0.2, diversity_weight: float = 0.2):
        """
        Initialize the recommender system.
        
        Args:
            db: SQLAlchemy database session
            min_reviews: Minimum number of total reviews required for a game to be recommended
            review_weight: Weight given to review ratio in final score (0-1)
            popularity_weight: Weight given to popularity (total reviews) in final score (0-1)
            diversity_weight: Weight given to diversity penalty in final score (0-1)
        """
        print("Initializing recommender")
        self.db = db
        self.min_reviews = min_reviews
        self.review_weight = review_weight
        self.popularity_weight = popularity_weight
        self.diversity_weight = diversity_weight
        
        # Get all games that meet minimum review threshold
        self.games = db.query(Game).filter(Game.total_reviews >= min_reviews).all()
        
        # Convert to DataFrame for easier processing
        self.df = pd.DataFrame([{
            'appid': g.appid,
            'name': g.name,
            'description': g.detailed_description or g.short_description or '',
            'tags': ' '.join(g.tags) if g.tags else '',
            'genres': ' '.join(g.genres) if g.genres else '',
            'developer': ' '.join(g.developer) if g.developer else 'Unknown',
            'publisher': ' '.join(g.publisher) if g.publisher else 'Unknown',
            'review_ratio': g.review_ratio,
            'popularity_score': g.popularity_score
        } for g in self.games])
        
        # Create feature transformers
        self.description_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.tags_vectorizer = TfidfVectorizer(max_features=1000)
        self.genres_vectorizer = TfidfVectorizer(max_features=100)
        self.developer_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
        self.publisher_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
        
        # Fit transformers
        self.description_matrix = self.description_vectorizer.fit_transform(self.df["description"])
        self.tags_matrix = self.tags_vectorizer.fit_transform(self.df["tags"])
        self.genres_matrix = self.genres_vectorizer.fit_transform(self.df["genres"])
        self.developer_matrix = self.developer_encoder.fit_transform(self.df[["developer"]])
        self.publisher_matrix = self.publisher_encoder.fit_transform(self.df[["publisher"]])
        
        # Combine all feature matrices
        from scipy.sparse import hstack
        self.feature_matrix = hstack([
            self.description_matrix,
            self.tags_matrix,
            self.genres_matrix,
            self.developer_matrix,
            self.publisher_matrix
        ])

    def recommend(self, user_games: List[Dict[str, Any]], top_n: int = 10, user_preferences: Dict[str, str] = None) -> List[Dict[str, Any]]:
        if not user_games:
            return []

        # Build user profile
        user_game_ids = {int(g["appid"]): float(g["playtime_forever"]) for g in user_games}
        
        # Find indices of user's games that exist in our filtered dataset
        user_game_mask = self.df["appid"].isin(user_game_ids)
        user_game_idxs = self.df[user_game_mask].index.tolist()
        
        if not user_game_idxs:
            return []

        # Get user's preferred developers
        user_developers = set(self.df.loc[user_game_idxs, "developer"].unique())
        
        # Normalize playtimes
        playtimes = []
        for idx in user_game_idxs:
            appid = int(self.df.loc[idx, "appid"])
            if appid in user_game_ids:
                playtime = min(user_game_ids[appid] / 6000, 1.0)  # 100h = 6000min
                # Adjust playtime based on user preference if it exists
                if user_preferences and str(appid) in user_preferences:
                    if user_preferences[str(appid)] == "disliked":
                        playtime *= 0.1  # Significantly reduce score for disliked games
                    elif user_preferences[str(appid)] == "liked":
                        playtime *= 1.5  # Boost score for liked games
                playtimes.append(playtime)
            else:
                playtimes.append(0.0)
        
        playtimes = np.array(playtimes)
        X_train = self.feature_matrix[user_game_idxs]
        y_train = playtimes

        # Train regression model
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        # Predict content-based scores
        user_owned = set(user_game_ids.keys())
        # Also exclude games that user has explicitly disliked
        if user_preferences:
            disliked_games = {int(appid) for appid, status in user_preferences.items() if status == "disliked"}
            user_owned.update(disliked_games)
            
        unseen_mask = ~self.df["appid"].isin(user_owned)
        unseen_idxs = self.df[unseen_mask].index.tolist()
        
        if not unseen_idxs:
            return []
            
        X_test = self.feature_matrix[unseen_idxs]
        content_scores = model.predict(X_test)
        
        # Get review scores and popularity scores
        review_scores = self.df.loc[unseen_idxs, 'review_ratio'].values
        popularity_scores = self.df.loc[unseen_idxs, 'popularity_score'].values
        
        # Calculate diversity penalty
        unseen_developers = self.df.loc[unseen_idxs, "developer"].values
        diversity_penalty = np.array([0.5 if dev in user_developers else 0.0 for dev in unseen_developers])
        
        # Apply preference boost for liked games
        preference_boost = np.ones(len(unseen_idxs))
        if user_preferences:
            for i, idx in enumerate(unseen_idxs):
                appid = int(self.df.loc[idx, "appid"])
                if str(appid) in user_preferences and user_preferences[str(appid)] == "liked":
                    preference_boost[i] = 1.5  # Boost score for liked games
        
        # Combine scores with weighted average
        final_scores = (
            (1 - self.review_weight - self.popularity_weight - self.diversity_weight) * content_scores +
            self.review_weight * review_scores +
            self.popularity_weight * popularity_scores -
            self.diversity_weight * diversity_penalty
        ) * preference_boost

        # Get top N recommendations
        top_n = min(top_n, len(final_scores))
        top_indices = np.argsort(final_scores)[-top_n:][::-1]
        top_game_idxs = [unseen_idxs[i] for i in top_indices]

        # Get full game data from database
        recommended_games = []
        for idx in top_game_idxs:
            appid = int(self.df.loc[idx, "appid"])
            game = self.db.query(Game).filter(Game.appid == appid).first()
            if game:
                recommended_games.append({
                    "appid": str(game.appid),
                    "name": game.name,
                    "releaseDate": game.release_date,
                    "detailedDescription": game.detailed_description,
                    "shortDescription": game.short_description,
                    "headerImage": game.header_image,
                    "developer": ' '.join(game.developer) if game.developer else "Unknown",
                    "publisher": ' '.join(game.publisher) if game.publisher else "Unknown",
                    "screenshots": game.screenshots if game.screenshots else [],
                })

        return recommended_games