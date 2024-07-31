from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
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


class Lecture(Base):
    __tablename__ = 'lectures'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    difficulty = Column(Integer, index=True)
    topic = Column(String, index=True)
    image = Column(String, index=True)
    description = Column(Text, index=True)


class WritingTask(Base):
    __tablename__ = 'writing_tasks'

    id = Column(Integer, primary_key=True, index=True)
    lecture_id = Column(Integer, ForeignKey('lectures.id'), index=True)
    question = Column(Text, index=True)
    content = Column(Text, index=True)
    lecture = relationship('Lecture', back_populates='writing_tasks')


Lecture.writing_tasks = relationship(
    'WritingTask', order_by=WritingTask.id, back_populates='lecture')


class ComprehensionTask(Base):
    __tablename__ = 'comprehension_tasks'

    id = Column(Integer, primary_key=True, index=True)
    lecture_id = Column(Integer, ForeignKey('lectures.id'), index=True)
    question = Column(Text, index=True)
    content = Column(Text, index=True)
    conversation = Column(Text, index=True)
    options = Column(Text, index=True)  # JSON encoded list
    answer = Column(String, index=True)
    lecture = relationship('Lecture', back_populates='comprehension_tasks')


Lecture.comprehension_tasks = relationship(
    'ComprehensionTask', order_by=ComprehensionTask.id, back_populates='lecture')


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, index=True)
    user_level = Column(Integer, default=1)
    grow = Column(String, index=True)
    purpose = Column(String, index=True)
    theme = Column(Text)


class Ranking(Base):
    __tablename__ = 'rankings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tier = Column(String, nullable=False)
    point = Column(Integer, nullable=False)

    #user = relationship('User', back_populates='rankings')
