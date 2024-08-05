from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional, List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    login_id: str


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     login_id = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     nickname = Column(String, unique=True, nullable=False)
#     profile_image = Column(String)
#     quiz_learning_history = Column(Text, default='{}')
#     Lecture_learning_history = Column(Text, default='{}')
#     total_learning_time = Column(Float, default=0.0)
#     level = Column(Integer, default=1)
#     exp = Column(Integer, default=1)
#     subscription = Column(Boolean, default=False)
#     signupdate = Column(DateTime, default=datetime.utcnow)
#     attendance = Column(Integer, default=0)
#     voca_list = relationship(
#         'Voca', secondary=user_voca_association, back_populates='users')
#     # 테스트 저장

class User(BaseModel):
    id: int
    login_id: str
    password: str
    nickname: str
    profile_image: Optional[str] = None
    quiz_learning_history: Optional[str] = None
    lecture_learning_history: Optional[str] = None
    total_learning_time: Optional[float] = 0.0
    level: Optional[int] = 1
    exp: Optional[int] = 0
    subscription: Optional[bool] = False
    attendance: Optional[int] = 0
    signupdate: Optional[datetime] = datetime.utcnow()


class UserCreate(BaseModel):
    login_id: str
    password1: str
    password2: str
    nickname: str
    profile_image: Optional[str] = None
    quiz_learning_history: Optional[str] = None
    lecture_learning_history: Optional[str] = None
    total_learning_time: Optional[float] = 0.0
    level: Optional[int] = 1
    exp: Optional[int] = 0
    subscription: Optional[bool] = False
    signupdate: Optional[datetime] = datetime.utcnow()
    attendance: Optional[int] = 0

    @field_validator("login_id", "nickname", "password1", "password2")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("입력되지 않은 항목이 있습니다.")
        return v

    @field_validator("password2")
    def password_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v


class UserUpdate(BaseModel):
    id: int
    login_id: Optional[str]
    password: Optional[str]
    nickname: Optional[str]
    profile_image: Optional[str]
    learning_history: Optional[str]
    total_learning_time: Optional[float]
    level: Optional[int]
    ranking_score: Optional[float]
    subscription: Optional[bool]
    ranking: Optional[int]
    attendance: Optional[int]


class UserDelete(BaseModel):
    id: int


class vocaList(BaseModel):
    user_id: int
    quiz_id: int

class UserResponse(BaseModel):
    id: int
    lecture_learning_history: str

    class Config:
        orm_mode = True

class LectureResponse(BaseModel):
    id: int
    title: str
    topic: str

    class Config:
        orm_mode = True