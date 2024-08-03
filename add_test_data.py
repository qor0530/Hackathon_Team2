from sqlalchemy.orm import Session
from config.database import SessionLocal, init_db
from api.models import Ranking, Tier, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def add_test_data():
    db: Session = SessionLocal()
    test_users = []

    tiers = [
        Tier.iron, Tier.bronze, Tier.silver, 
        Tier.gold, Tier.platinum, Tier.emerald, 
        Tier.diamond, Tier.master
    ]

    names = [
        "John", "James", "Robert", "Michael", "William",
        "David", "Richard", "Joseph", "Thomas", "Charles",
        "Mary", "Patricia", "Linda", "Barbara", "Elizabeth",
        "Jennifer", "Maria", "Susan", "Margaret", "Dorothy",
        "Christopher", "Daniel", "Paul", "Mark", "Donald",
        "George", "Kenneth", "Steven", "Edward", "Brian",
        "Ronald", "Anthony", "Kevin", "Jason", "Matthew",
        "Gary", "Timothy", "Jose", "Larry", "Jeffrey",
        "Sandra", "Carol", "Ruth", "Sharon", "Michelle",
        "Laura", "Sarah", "Kimberly", "Deborah", "Jessica",
        "Shirley", "Cynthia", "Angela", "Melissa", "Brenda",
        "Amy", "Anna", "Rebecca", "Virginia", "Kathleen",
        "Emma", "Olivia", "Ava", "Isabella", "Sophia",
        "Mia", "Charlotte", "Amelia", "Evelyn", "Abigail",
        "Harper", "Emily", "Ella", "Lily", "Sofia",
        "Avery", "Mila", "Aria", "Scarlett", "Penelope",
        "Layla", "Chloe", "Victoria", "Madison", "Eleanor",
        "Grace", "Nora", "Riley", "Zoey", "Hannah"
    ]

    used_nicknames = set()

    # Ensure there are enough unique names for all users
    total_users = len(tiers) * 10
    if total_users > len(names):
        raise ValueError("Not enough unique names available for the number of users")

    user_id = 1
    name_index = 0
    for tier in tiers:
        for i in range(5):
            nickname = names[name_index]
            name_index += 1
            test_users.append({"user_id": user_id, "score": 100 * user_id, "tier": tier, "nickname": nickname})
            user_id += 1
        for i in range(5):
            nickname = names[name_index]
            name_index += 1
            test_users.append({"user_id": user_id, "score": 100 * (user_id + 100), "tier": tier, "nickname": nickname})
            user_id += 1

    for user_data in test_users:
        existing_user = db.query(Ranking).filter(Ranking.user_id == user_data["user_id"]).first()
        if existing_user:
            existing_user.score += user_data["score"]
        else:
            new_user = Ranking(user_id=user_data["user_id"], score=user_data["score"], tier=user_data["tier"])
            db.add(new_user)
        
        # Create corresponding User entry if not exists
        existing_user_entry = db.query(User).filter(User.id == user_data["user_id"]).first()
        if not existing_user_entry:
            hashed_password = hash_password("password")
            new_user_entry = User(
                id=user_data["user_id"], 
                nickname=user_data["nickname"], 
                login_id=f"user{user_data['user_id']}", 
                password=hashed_password
            )
            db.add(new_user_entry)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    add_test_data()
    print("Test data added")
