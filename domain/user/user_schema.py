from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    login_id: str


class UserCreate(BaseModel):
    login_id: str
    password1: str
    password2: str
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