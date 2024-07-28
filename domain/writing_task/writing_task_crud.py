from sqlalchemy.orm import Session
from api.models import WritingTask
from domain.writing_task.writing_task_schema import WritingTaskCreate, WritingTaskUpdate


def get_writing_task_list(db: Session):
    writing_task_list = db.query(WritingTask).all()
    return writing_task_list


def get_writing_task(db: Session, writing_task_id: int):
    writing_task = db.query(WritingTask).get(writing_task_id)
    return writing_task


def create_writing_task(db: Session, writing_task_create: WritingTaskCreate):
    db_writing_task = WritingTask(
        lecture_id=writing_task_create.lecture_id,
        question=writing_task_create.question,
        content=writing_task_create.content
    )
    db.add(db_writing_task)
    db.commit()
    db.refresh(db_writing_task)
    return db_writing_task


def update_writing_task(db: Session, db_writing_task: WritingTask, writing_task_update: WritingTaskUpdate):
    db_writing_task.lecture_id = writing_task_update.lecture_id
    db_writing_task.question = writing_task_update.question
    db_writing_task.content = writing_task_update.content
    db.add(db_writing_task)
    db.commit()
    db.refresh(db_writing_task)
    return db_writing_task


def delete_writing_task(db: Session, db_writing_task: WritingTask):
    db.delete(db_writing_task)
    db.commit()
    db.refresh(db_writing_task)
    return db_writing_task
