from sqlalchemy.orm import Session
from api.models import Lecture
from domain.lecture.lecture_schema import LectureCreate, LectureUpdate


def get_lecture_list(db: Session):
    lecture_list = db.query(Lecture).all()
    return lecture_list


def get_lecture(db: Session, lecture_id: int):
    lecture = db.query(Lecture).get(lecture_id)
    return lecture


def create_lecture(db: Session, lecture_create: LectureCreate):
    db_lecture = Lecture(title=lecture_create.title,
                         difficulty=lecture_create.difficulty, topic=lecture_create.topic)
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture


def update_lecture(db: Session, db_lecture: Lecture, lecture_update: LectureUpdate):
    db_lecture.title = lecture_update.title
    db_lecture.difficulty = lecture_update.difficulty
    db_lecture.topic = lecture_update.topic
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture


def delete_lecture(db: Session, db_lecture: Lecture):
    db.delete(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture
