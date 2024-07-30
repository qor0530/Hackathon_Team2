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
    return db_User


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.login_id = user_update.login_id
    db_user.password = user_update.password
    db_user.nickname = user_update.nickname
    db_user.profile_image = user_update.profile_image
    db_user.learning_history = user_update.learning_history
    db_user.total_learning_time = user_update.total_learning_time
    db_user.level = user_update.level
    db_user.ranking_score = user_update.ranking_score
    db_user.subscription = user_update.subscription
    db_user.ranking = user_update.ranking
    db_user.attendance = user_update.attendance
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    db.refresh(db_user)
