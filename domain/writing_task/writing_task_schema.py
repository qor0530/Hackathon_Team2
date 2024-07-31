from pydantic import BaseModel


class WritingTaskBase(BaseModel):
    lecture_id: int
    question: str
    content: str


class WritingTaskCreate(WritingTaskBase):
    pass


class WritingTaskUpdate(WritingTaskBase):
    pass


class WritingTask(WritingTaskBase):
    id: int

    class Config:
        orm_mode = True
