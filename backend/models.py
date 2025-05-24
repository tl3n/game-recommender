from sqlalchemy import Column, Integer, String, ForeignKey, Enum, create_engine, UniqueConstraint, JSON, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class GameStatus(enum.Enum):
    LIKED = "liked"
    DISLIKED = "disliked"

class Game(Base):
    __tablename__ = "games"

    appid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    release_date = Column(String)
    detailed_description = Column(String)
    short_description = Column(String)
    header_image = Column(String)
    screenshots = Column(JSON)  # Store as JSON array
    genres = Column(JSON)  # Store as JSON array
    tags = Column(JSON)  # Store as JSON array
    positive = Column(Integer, default=0)
    negative = Column(Integer, default=0)
    developer = Column(JSON)  # Store as JSON array
    publisher = Column(JSON)  # Store as JSON array
    total_reviews = Column(Integer, default=0)
    review_ratio = Column(Float, default=0.0)
    popularity_score = Column(Float, default=0.0)

class UserGamePreference(Base):
    __tablename__ = "user_game_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    steam_id = Column(String, nullable=False, index=True)
    appid = Column(String, nullable=False)
    status = Column(Enum(GameStatus), nullable=False)

    # Create a composite unique constraint to ensure one status per game per user
    __table_args__ = (
        UniqueConstraint('steam_id', 'appid', name='uq_user_game'),
    )

# Create tables
def init_db(database_url="sqlite:///./game_recommender.db"):
    engine = create_engine(database_url)
    print("Created engine")
    Base.metadata.create_all(engine)
    print("Create all")
    return engine 