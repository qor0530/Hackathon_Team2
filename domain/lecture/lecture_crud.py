from sqlalchemy.orm import Session
from api.models import Lecture, WritingTask, ComprehensionTask
from domain.lecture.lecture_schema import LectureCreate, LectureUpdate


def get_lecture_list(db: Session):
    return db.query(Lecture).all()


def get_lecture(db: Session, lecture_id: int):
    return db.query(Lecture).get(lecture_id)


def create_lecture(db: Session, lecture_create: LectureCreate):
    db_lecture = Lecture(
        title=lecture_create.title,
        difficulty=lecture_create.difficulty,
        topic=lecture_create.topic,
        image=lecture_create.image,
        description=lecture_create.description
    )
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)

    if lecture_create.type == "writing":
        db_task = WritingTask(
            lecture_id=db_lecture.id,
            question=lecture_create.question,
            content=lecture_create.content
        )
    elif lecture_create.type == "comprehension":
        db_task = ComprehensionTask(
            lecture_id=db_lecture.id,
            question=lecture_create.question,
            content=lecture_create.content,
            conversation=lecture_create.conversation,
            options=lecture_create.options,
            answer=lecture_create.answer
        )
    db.add(db_task)
    db.commit()
    return db_lecture


def update_lecture(db: Session, db_lecture: Lecture, lecture_update: LectureUpdate):
    db_lecture.title = lecture_update.title
    db_lecture.difficulty = lecture_update.difficulty
    db_lecture.topic = lecture_update.topic
    db_lecture.image = lecture_update.image
    db_lecture.description = lecture_update.description
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)

    if lecture_update.type == "writing":
        db_task = db.query(WritingTask).filter(
            WritingTask.lecture_id == db_lecture.id).first()
        if db_task:
            db_task.question = lecture_update.question
            db_task.content = lecture_update.content
    elif lecture_update.type == "comprehension":
        db_task = db.query(ComprehensionTask).filter(
            ComprehensionTask.lecture_id == db_lecture.id).first()
        if db_task:
            db_task.question = lecture_update.question
            db_task.content = lecture_update.content
            db_task.conversation = lecture_update.conversation
            db_task.options = lecture_update.options
            db_task.answer = lecture_update.answer
    db.add(db_task)
    db.commit()
    return db_lecture


def delete_lecture(db: Session, db_lecture: Lecture):
    db.delete(db_lecture)
    db.commit()
    return db_lecture
