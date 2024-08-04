from sqlalchemy.orm import Session
from api.models import Ranking, Tier

def get_rankings(db: Session):
    return db.query(Ranking).order_by(Ranking.score.desc()).all()

def update_user_tier(db: Session, user_id: int, new_tier: Tier):
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if user:
        user.tier = new_tier
        db.commit()
        db.refresh(user)
    return user

def update_user_score(db: Session, user_id: int, score: int):
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if user:
        user.score += score
        db.commit()
        db.refresh(user)
    return user

def get_users_by_tier(db: Session, tier: Tier):
    return db.query(Ranking).filter(Ranking.tier == tier).order_by(Ranking.score.desc()).all()

def get_user_tier_by_user_id(db: Session, user_id: int):
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if user:
        return user.tier
    return None

def get_user_score_by_user_id(db: Session, user_id: int):
    user = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if user:
        return user.score
    return None

