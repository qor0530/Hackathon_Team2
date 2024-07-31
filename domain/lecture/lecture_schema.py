from pydantic import BaseModel


class LectureBase(BaseModel):
    title: str
    difficulty: str
    topic: str
    image: str
    description: str


class LectureCreate(LectureBase):
    type: str
    question: str = None
    content: str = None
    conversation: str = None
    options: str = None
    answer: int = None


class LectureUpdate(LectureBase):
    type: str
    question: str = None
    content: str = None
    conversation: str = None
    options: str = None
    answer: int = None


class Lecture(LectureBase):
    id: int

    class Config:
        orm_mode = True
