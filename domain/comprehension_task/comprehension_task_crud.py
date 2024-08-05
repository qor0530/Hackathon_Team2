from sqlalchemy.orm import Session
from api.models import ComprehensionTask
from domain.comprehension_task.comprehension_task_schema import ComprehensionTaskCreate, ComprehensionTaskUpdate


def get_comprehension_task_list(db: Session):
    comprehension_task_list = db.query(ComprehensionTask).all()
    return comprehension_task_list


def get_comprehension_task(db: Session, comprehension_task_id: int):
    comprehension_task = db.query(ComprehensionTask).get(comprehension_task_id)
    return comprehension_task


def create_comprehension_task(db: Session, comprehension_task_create: ComprehensionTaskCreate):
    db_comprehension_task = ComprehensionTask(
        lecture_id=comprehension_task_create.lecture_id,
        question=comprehension_task_create.question,
        content=comprehension_task_create.content,
        conversation=comprehension_task_create.conversation,
        options=comprehension_task_create.options,
        answer=comprehension_task_create.answer
    )
    db.add(db_comprehension_task)
    db.commit()
    db.refresh(db_comprehension_task)
    return db_comprehension_task


def update_comprehension_task(db: Session, db_comprehension_task: ComprehensionTask, comprehension_task_update: ComprehensionTaskUpdate):
    db_comprehension_task.lecture_id = comprehension_task_update.lecture_id
    db_comprehension_task.question = comprehension_task_update.question
    db_comprehension_task.content = comprehension_task_update.content
    db_comprehension_task.conversation = comprehension_task_update.conversation
    db_comprehension_task.options = comprehension_task_update.options
    db_comprehension_task.answer = comprehension_task_update.answer
    db.add(db_comprehension_task)
    db.commit()
    db.refresh(db_comprehension_task)
    return db_comprehension_task


def delete_comprehension_task(db: Session, db_comprehension_task: ComprehensionTask):
    db.delete(db_comprehension_task)
    db.commit()
    db.refresh(db_comprehension_task)
    return db_comprehension_task
