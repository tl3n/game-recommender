# recommender.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

class Recommender:
    def __init__(self, metadata_df: pd.DataFrame, min_reviews: int = 100, review_weight: float = 0.3, 
                 popularity_weight: float = 0.2, diversity_weight: float = 0.2):
        """
        Initialize the recommender system.
        
        Args:
            metadata_df: DataFrame containing game metadata
            min_reviews: Minimum number of total reviews required for a game to be recommended
            review_weight: Weight given to review ratio in final score (0-1)
            popularity_weight: Weight given to popularity (total reviews) in final score (0-1)
            diversity_weight: Weight given to diversity penalty in final score (0-1)
        """
        self.df = metadata_df.copy()
        self.min_reviews = min_reviews
        self.review_weight = review_weight
        self.popularity_weight = popularity_weight
        self.diversity_weight = diversity_weight
        
        # Calculate review ratios and popularity scores
        self.df['total_reviews'] = self.df['positive'] + self.df['negative']
        self.df['review_ratio'] = self.df['positive'] / (self.df['total_reviews'] + 1e-6)
        
        # Normalize popularity scores (total reviews) to 0-1 range
        max_reviews = self.df['total_reviews'].max()
        self.df['popularity_score'] = self.df['total_reviews'] / (max_reviews + 1e-6)
        
        # Filter out games with insufficient reviews
        self.df = self.df[self.df['total_reviews'] >= min_reviews].copy()
        self.df = self.df.reset_index(drop=True)
        
        # Prepare features for vectorization
        # Ensure tags and genres are lists and convert to space-separated strings
        self.df['tags'] = self.df['tags'].apply(
            lambda x: " ".join(x) if isinstance(x, (list, tuple, set)) else str(x) if pd.notna(x) else ""
        )
        self.df['genres'] = self.df['genres'].apply(
            lambda x: " ".join(x) if isinstance(x, (list, tuple, set)) else str(x) if pd.notna(x) else ""
        )
        
        # Fill NaN values for developer and publisher and ensure they are strings
        self.df['developer'] = self.df['developer'].apply(
            lambda x: " ".join(x) if isinstance(x, (list, tuple, set)) else str(x) if pd.notna(x) else "Unknown"
        )
        self.df['publisher'] = self.df['publisher'].apply(
            lambda x: " ".join(x) if isinstance(x, (list, tuple, set)) else str(x) if pd.notna(x) else "Unknown"
        )
        
        # Create feature transformers
        self.description_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.tags_vectorizer = TfidfVectorizer(max_features=1000)
        self.genres_vectorizer = TfidfVectorizer(max_features=100)
        self.developer_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
        self.publisher_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
        
        # Fit transformers
        self.description_matrix = self.description_vectorizer.fit_transform(self.df["description"].fillna(""))
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

    def recommend(self, user_games: list, top_n: int = 10):
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
        
        # Combine scores with weighted average
        final_scores = (
            (1 - self.review_weight - self.popularity_weight - self.diversity_weight) * content_scores +
            self.review_weight * review_scores +
            self.popularity_weight * popularity_scores -
            self.diversity_weight * diversity_penalty
        )

        # Get top N recommendations
        top_n = min(top_n, len(final_scores))
        top_indices = np.argsort(final_scores)[-top_n:][::-1]
        top_game_idxs = [unseen_idxs[i] for i in top_indices]

        return [
            {
                "title": str(self.df.loc[i, "name"]),
                "appid": int(self.df.loc[i, "appid"]),
                "developer": str(self.df.loc[i, "developer"]),
                "score": float(final_scores[top_indices[j]]),
                "review_ratio": float(self.df.loc[i, "review_ratio"]),
                "total_reviews": int(self.df.loc[i, "total_reviews"])
            }
            for j, i in enumerate(top_game_idxs)
        ]
