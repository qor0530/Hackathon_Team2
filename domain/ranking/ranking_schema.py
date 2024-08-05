from sqlalchemy import Column, Integer, Enum as SqlEnum
from config.database import Base
import enum

class Tier(enum.Enum):
    iron = "iron"
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
    emerald = "emerald"
    diamond = "diamond"
    master = "master"

class Ranking(Base):
    __tablename__ = "rankings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    score = Column(Integer)
    tier = Column(SqlEnum(Tier), default=Tier.iron)
