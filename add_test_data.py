from sqlalchemy.orm import Session
from config.database import SessionLocal, init_db
from api.models import Ranking, Tier

def add_test_data():
    db: Session = SessionLocal()
    test_users = []

    tiers = [
        Tier.iron, Tier.bronze, Tier.silver, 
        Tier.gold, Tier.platinum, Tier.emerald, 
        Tier.diamond, Tier.master
    ]

    user_id = 1
    for tier in tiers:
        for i in range(5):
            test_users.append({"user_id": user_id, "score": 100 * user_id, "tier": tier})
            user_id += 1
        for i in range(5):
            test_users.append({"user_id": user_id, "score": 100 * (user_id + 100), "tier": tier})
            user_id += 1

    for user_data in test_users:
        existing_user = db.query(Ranking).filter(Ranking.user_id == user_data["user_id"]).first()
        if existing_user:
            existing_user.score += user_data["score"]
        else:
            new_user = Ranking(**user_data)
            db.add(new_user)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    add_test_data()
    print("Test data added")