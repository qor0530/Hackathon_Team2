from api.models import Quiz
from sqlalchemy.orm import Session

from domain.quiz.quiz_schema import QuizCreate, QuizUpdate


def get_quiz_list(db: Session):
    quiz_list = db.query(Quiz).all()  # 여기서 레벨에 따라 판정해도 됨.
    return quiz_list


def get_quiz(db: Session, quiz_id: int):
    quiz = db.query(Quiz).get(quiz_id)
    return quiz

    # <h2 > {{quiz.subject}} < /h2 >
    # <p > {{quiz.level}} < /p >
    # <p > {{quiz.sentence}} < /p >
    # <p > {{quiz.explanation}} < /p >
    # <p > {{quiz.answer}} < /p >
    # <p > {{quiz.hint}} < /p >
    # <p > {{quiz.answer_explanation}} < /p >


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
