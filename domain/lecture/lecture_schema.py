from pydantic import BaseModel


class LectureBase(BaseModel):
    title: str
    difficulty: str
    topic: str


class LectureCreate(LectureBase):
    pass


class LectureUpdate(LectureBase):
    pass


class Lecture(LectureBase):
    id: int

    class Config:
        orm_mode = True
