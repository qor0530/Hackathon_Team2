from api.models import User, Ranking
from sqlalchemy.orm import Session
from api.models import User
from .user_schema import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_list(db: Session):
    user_list = db.query(User).all()
    return user_list


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(User.login_id == user_create.login_id).first()


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user


def get_user_login_id(db: Session, login_id: str):
    return db.query(User).filter(User.login_id == login_id).first()


def create_user(db: Session, user_create: UserCreate):
    db_User = User(login_id=user_create.login_id,
                   password=pwd_context.hash(user_create.password1), nickname=user_create.nickname,
                   profile_image=user_create.profile_image, learning_history=user_create.learning_history,
                   total_learning_time=user_create.total_learning_time, level=user_create.level,
                   exp=user_create.exp,
                   subscription=user_create.subscription, attendance=user_create.attendance)

    db.add(db_User)
    db.commit()
    db.refresh(db_User)

    # Get the most recent ranking
    # latest_ranking = db.query(Ranking).order_by(Ranking.id.desc()).first()
    # if latest_ranking:
    #     latest_ranking.user_id = db_User.id
    #     db.add(latest_ranking)
    #     db.commit()
    #     db.refresh(latest_ranking)

    return db_User

def exp_edit(db: Session, db_user : User, exp: int):
    #여기에 exp 수정 로직 추가
    gain_exp = exp
    db_user.exp += gain_exp
    db.commit()
    db.refresh(db_user)