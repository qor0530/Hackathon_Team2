from sqlalchemy import *
from config.database import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, index=True)
    subject = Column(String, index=True)
    sentence = Column(Text, index=True)
    explanation = Column(Text, index=True)
    answer = Column(String, index=True)
    hint = Column(String, index=True)
    answer_explanation = Column(Text, index=True)


class User(Base):
    __tablename__ = 'users'
 
    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    profile_image = Column(String)
    learning_history = Column(Text)  
    total_learning_time = Column(Float, default=0.0) 
    level = Column(Integer, default=1)
    ranking_score = Column(Float, default=0.0)
    subscription = Column(Boolean, default=False)
    ranking = Column(Integer, default=0)
    attendance = Column(Integer, default=0)
