from domain.user.user_schema import UserCreate
from api.models import User, Ranking
from sqlalchemy.orm import Session
from api.models import User
from .user_schema import UserCreate, UserUpdate


def get_user_list(db: Session):
    user_list = db.query(User).all()
    return user_list


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user


def create_user(db: Session, user_create: UserCreate):
    db_User = User(login_id=user_create.login_id,
                   password=user_create.password, nickname=user_create.nickname,
                   profile_image=user_create.profile_image, learning_history=user_create.learning_history,
                   total_learning_time=user_create.total_learning_time, level=user_create.level,
                   ranking_score=user_create.ranking_score, subscription=user_create.subscription,
                   ranking=user_create.ranking, attendance=user_create.attendance)

    db.add(db_User)
    db.commit()
    db.refresh(db_User)

    # Get the most recent ranking
    latest_ranking = db.query(Ranking).order_by(Ranking.id.desc()).first()
    if latest_ranking:
        latest_ranking.user_id = db_User.id
        db.add(latest_ranking)
        db.commit()
        db.refresh(latest_ranking)

    return db_User
