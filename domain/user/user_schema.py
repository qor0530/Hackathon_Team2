from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    login_id: str


class UserBase(BaseModel):
    login_id: str
    password: str
    nickname: str
    profile_image: Optional[str] = None
    learning_history: Optional[str] = None
    total_learning_time: Optional[float] = 0.0
    level: Optional[int] = 1
    exp: Optional[int] = 0
    ranking_score: Optional[float] = 0.0
    subscription: Optional[bool] = False
    ranking: Optional[int] = 0
    attendance: Optional[int] = 0

    @field_validator("login_id", "nickname")
    def not_empty(cls, v):
        if not v:
            raise ValueError("빈값이 입력됨")
        return v


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v:
            raise ValueError("비밀번호는 필수 입력입니다.")
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
