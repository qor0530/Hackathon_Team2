from api.models import User, user_voca_association, Quiz, Lecture, Ranking
from sqlalchemy.orm import Session
from .user_schema import UserCreate, LectureResponse
from passlib.context import CryptContext
from fastapi import HTTPException
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# KAKAO_CLIENT_ID = 'zM9Xs2bB0fjQfVa72CKdkWDdAkC0oHo9AAAAAQo8JCAAAAGRHqq7q82yTeNnt1bO'
# KAKAO_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
# KAKAO_REDIRECT_URI = 'YOUR_REDIRECT_URI'


# def get_kakao_access_token(code: str) -> str:
#     url = "https://kauth.kakao.com/oauth/token"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     payload = {
#         "grant_type": "authorization_code",
#         "client_id": KAKAO_CLIENT_ID,
#         "client_secret": KAKAO_CLIENT_SECRET,
#         "redirect_uri": KAKAO_REDIRECT_URI,
#         "code": code,
#     }

#     response = httpx.post(url, headers=headers, data=payload)
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=400, detail="Failed to obtain access token")

#     return response.json()["access_token"]


# def get_kakao_user_info(access_token: str) -> dict:
#     url = "https://kapi.kakao.com/v2/user/me"
#     headers = {"Authorization": f"Bearer {access_token}"}

#     response = httpx.get(url, headers=headers)
#     if response.status_code != 200:
#         raise HTTPException(
#             status_code=400, detail="Failed to obtain user info")

#     return response.json()


# def get_or_create_user(db: Session, user_info: dict):
#     kakao_id = user_info["id"]
#     account_info = user_info["kakao_account"]
#     profile = account_info["profile"]

#     user = db.query(User).filter(User.login_id == kakao_id).first()
#     if user:
#         return user

#     new_user = User(
#         login_id=kakao_id,
#         password=pwd_context.hash("kakao_default_password"),  # 기본 비밀번호 설정
#         nickname=profile["nickname"],
#         profile_image=profile.get("profile_image_url"),
#         quiz_learning_history=json.dumps({}),
#         lecture_learning_history=json.dumps({}),
#         total_learning_time=0.0,
#         level=1,
#         exp=0,
#         subscription=False,
#         attendance=0,
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


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
                   profile_image=user_create.profile_image, quiz_learning_history=user_create.quiz_learning_history,
                   lecture_learning_history=user_create.lecture_learning_history,
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
    association = user_voca_association.insert().values(
        user_id=user_id, quiz_id=quiz_id)
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

# lecture 추천 관련


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_lectures_by_ids(db: Session, ids: list):
    return db.query(Lecture).filter(Lecture.id.in_(ids)).all()


def get_topic_counts(lectures):
    topic_count = {}
    for lecture in lectures:
        if lecture.topic in topic_count:
            topic_count[lecture.topic] += 1
        else:
            topic_count[lecture.topic] = 1
    return topic_count


def get_most_frequent_topic(topic_count):
    if not topic_count:
        return None
    return max(topic_count, key=topic_count.get)


def get_lectures_by_topic(db: Session, topic: str, excluded_ids: list):
    return db.query(Lecture).filter(
        Lecture.topic == topic,
        Lecture.id.not_in(excluded_ids)
    ).all()


def parse_learning_history(learning_history: str):
    try:
        # Remove any extra whitespace and split by comma
        ids_str = learning_history.strip().split(',')
        # Convert to integer list
        return [int(id_str.strip()) for id_str in ids_str if id_str.strip().isdigit()]
    except ValueError:
        return []


def add_incorrect_quiz(db: Session, user_id: int, quiz_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 기존의 incorrect_quizzes를 가져와서 쉼표로 분리
    incorrect_quizzes = user.incorrect_quizzes.split(',')
    incorrect_quizzes = [quiz.strip()
                         for quiz in incorrect_quizzes if quiz.strip()]

    # 이미 존재하지 않는 경우에만 추가
    if str(quiz_id) not in incorrect_quizzes:
        incorrect_quizzes.append(str(quiz_id))
        user.incorrect_quizzes = ','.join(incorrect_quizzes)
        db.commit()


def add_quiz_to_learning_history(db: Session, user: User, quiz_id: int):
    try:
        if user.quiz_learning_history is None:
            user.quiz_learning_history = ""

        quiz_ids = user.quiz_learning_history.split(
            ",") if user.quiz_learning_history else []

        if str(quiz_id) not in quiz_ids:
            quiz_ids.append(str(quiz_id))
            user.quiz_learning_history = ",".join(quiz_ids)

            # Ranking 객체를 가져와서 점수 업데이트
            print("여기되니")
            ranking = db.query(Ranking).filter(
                Ranking.user_id == user.id).first()

            if ranking:
                ranking.score += 100
            else:
                # 만약 Ranking 객체가 없다면 새로 생성
                new_ranking = Ranking(user_id=user.id, score=100)
                db.add(new_ranking)

            db.commit()
        else:
            pass
            # logging.info(
            #     f"Quiz ID {quiz_id} already in user's learning history.")
    except Exception as e:
        pass
        # logging.error(
        #     f"Failed to add quiz to learning history and update score: {e}")
        # raise


def add_lecture_to_learning_history(db: Session, user: User, lecture_id: int):
    try:
        if user.lecture_learning_history is None:
            user.lecture_learning_history = ""

        lecture_ids = user.lecture_learning_history.split(
            ",") if user.lecture_learning_history else []

        if str(lecture_id) not in lecture_ids:
            lecture_ids.append(str(lecture_id))
            user.lecture_learning_history = ",".join(lecture_ids)

            db.commit()
        else:
            pass
    except Exception as e:
        pass


def add_quiz_to_today_current(db: Session, user: User, lecture_id: int):
    try:
        if user.today_current_quiz is None:
            user.today_current_quiz = ""

        lecture_ids = user.today_current_quiz.split(
            ",") if user.today_current_quiz else []

        if str(lecture_id) not in lecture_ids:
            lecture_ids.append(str(lecture_id))
            user.lecture_learning_history = ",".join(lecture_ids)

            db.commit()
        else:
            pass
    except Exception as e:
        pass
