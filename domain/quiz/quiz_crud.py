import random
from api.models import Quiz, User
from sqlalchemy.orm import Session
from domain.quiz.quiz_schema import QuizCreate, QuizUpdate
from sqlalchemy import func


def get_quiz_list(db: Session):
    quiz_list = db.query(Quiz).all()
    return quiz_list


def get_quiz(db: Session, quiz_id: int):
    quiz = db.query(Quiz).get(quiz_id)
    return quiz


def create_quiz(db: Session, quiz_create: QuizCreate):
    db_quiz = Quiz(level=quiz_create.level, subject=quiz_create.subject, sentence=quiz_create.sentence, explanation=quiz_create.explanation,
                   answer=quiz_create.answer, hint=quiz_create.hint, answer_explanation=quiz_create.answer_explanation)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def update_quiz(db: Session, db_quiz: Quiz, quiz_update: QuizUpdate):
    db_quiz.level = quiz_update.level
    db_quiz.subject = quiz_update.subject
    db_quiz.sentence = quiz_update.sentence
    db_quiz.explanation = quiz_update.explanation
    db_quiz.answer = quiz_update.answer
    db_quiz.hint = quiz_update.hint
    db_quiz.answer_explanation = quiz_update.answer_explanation
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)


def delete_quiz(db: Session, db_quiz: Quiz):
    db.delete(db_quiz)
    db.commit()
    db.refresh(db_quiz)


def get_quizzes_by_type(db: Session, user_id: int, quiz_type: str, limit: int = 10):
    if quiz_type == "random":
        quizzes = db.query(Quiz).order_by(func.random()).limit(limit).all()
    elif quiz_type == "incorrect":
        user = db.query(User).filter_by(id=user_id).first()
        if user and user.incorrect_quizzes:
            incorrect_ids = eval(user.incorrect_quizzes)
            quizzes = db.query(Quiz).filter(
                Quiz.id.in_(incorrect_ids)).limit(limit).all()
        else:
            quizzes = []
    elif quiz_type == "level":
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            user_level = user.level
            quizzes = db.query(Quiz).filter(Quiz.level.between(
                user_level - 1, user_level + 1)).limit(limit).all()
        else:
            quizzes = []
    else:
        quizzes = []
    return quizzes

