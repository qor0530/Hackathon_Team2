from api.models import User, Ranking, user_voca_association, Quiz
from sqlalchemy.orm import Session
from api.models import User
from .user_schema import UserCreate, UserUpdate
from passlib.context import CryptContext
from fastapi import HTTPException

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


def exp_edit(db: Session, db_user: User, change_exp: int):
    # 여기에 exp 수정 로직 추가
    db_user.exp = change_exp
    db.commit()
    db.refresh(db_user)

# user_crud.py
def get_login_ids(db: Session):
    return db.query(User.login_id).all()

#####################
## voca 관련 라우터 ##
#####################

def get_voca_list(db: Session, user_id: int):
    # 유저가 존재하는지 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []

    # user_voca_association 테이블을 통해 해당 유저의 quiz_id 목록 가져오기
    quiz_ids = (
        db.query(user_voca_association.c.quiz_id)
        .filter(user_voca_association.c.user_id == user_id)
        .all()
    )

    # quiz_ids를 리스트로 변환
    quiz_ids = [quiz_id for (quiz_id,) in quiz_ids]

    # quiz_ids에 해당하는 Quiz 객체들 가져오기
    quizzes = db.query(Quiz).filter(Quiz.id.in_(quiz_ids)).all()

    # Quiz 객체들을 JSON 직렬화 가능하게 변환
    quizzes_list = [{"id": quiz.id, "level": quiz.level, "subject": quiz.subject,
                     "sentence": quiz.sentence, "explanation": quiz.explanation,
                     "answer": quiz.answer, "hint": quiz.hint,
                     "answer_explanation": quiz.answer_explanation} for quiz in quizzes]

    return quizzes_list

def add_quiz_to_user_voca(db: Session, user_id: int, quiz_id: int):
    # 유저와 퀴즈 존재 여부 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise print("User not found")
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise print("Quiz not found")

    # association 테이블에 추가
    association = user_voca_association.insert().values(user_id=user_id, quiz_id=quiz_id)
    db.execute(association)
    db.commit()

    return {"message": "Quiz added to user voca list"}


def delete_quiz_from_user_voca(db: Session, user_id: int, quiz_id: int):
    # user_voca_association 테이블에서 특정 유저와 quiz_id의 레코드 삭제
    association = db.query(user_voca_association).filter(
        user_voca_association.c.user_id == user_id,
        user_voca_association.c.quiz_id == quiz_id
    ).first()
    
    if not association:
        raise HTTPException(status_code=404, detail="Association not found")

    db.query(user_voca_association).filter(
        user_voca_association.c.user_id == user_id,
        user_voca_association.c.quiz_id == quiz_id
    ).delete()
    
    db.commit()

    return {"message": "Quiz deleted from user voca list"}


