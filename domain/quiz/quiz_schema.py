from pydantic import BaseModel, field_validator
from typing import Optional

# class Quiz(Base):
#     __tablename__ = 'quizzes'

#     id = Column(Integer, primary_key=True, index=True)
#     level = Column(Integer, index=True)
#     subject = Column(String, index=True)
#     sentence = Column(Text, index=True)
#     explanation = Column(Text, index=True)
#     answer = Column(String, index=True)
#     hint = Column(String, index=True)
#     answer_explanation = Column(Text, index=True)


class Quiz(BaseModel):
    id: int
    level: int
    subject: str
    sentence: str
    expalanation: str
    answer: str
    hint: str
    answer_explanation: str


class QuizCreate(BaseModel):
    level: int
    subject: str
    sentence: str
    explanation: str
    answer: str
    hint: str
    answer_explanation: str

    @field_validator("level", "subject", "sentence", "explanation", "answer", "hint", "answer_explanation")
    def not_empty(cls, v):
        print(v, type(v))
        if not v:
            raise ValueError("빈값이 입력됨")
        return v


class QuizUpdate(BaseModel):
    id: int
    subject: Optional[str]
    level: Optional[str]
    sentence: Optional[str]
    explanation: Optional[str]
    answer: Optional[str]
    hint: Optional[str]
    answer_explanation: Optional[str]
