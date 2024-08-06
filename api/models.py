import logging
from collections import Counter
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, event, Enum as SqlEnum, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy import *
from config.database import Base
import enum
from datetime import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


user_voca_association = Table(
    'user_voca_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('quiz_id', Integer, ForeignKey('voca.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    profile_image = Column(String)
    quiz_learning_history = Column(Text, default='')
    lecture_learning_history = Column(Text, default='')
    total_learning_time = Column(Float, default=0.0)
    incorrect_quizzes = Column(Text, default='')
    quiz_stack = Column(Text, default='')
    today_current_quiz = Column(Text, default='')
    # today_incurrent_quiz = Column(Text, default='')
    level = Column(Integer, default=1)
    exp = Column(Integer, default=1)
    subscription = Column(Boolean, default=False)
    signupdate = Column(DateTime, default=datetime.utcnow)
    attendance = Column(Integer, default=0)
    voca_list = relationship(
        'Voca', secondary=user_voca_association, back_populates='users')
    # 테스트 저장

    def update_level(self):
        if self.exp < 100:
            self.level = 1
        elif self.exp < 300:
            self.level = 2
        elif self.exp < 600:
            self.level = 3
        elif self.exp < 1100:
            self.level = 4
        else:
            self.level = 5


@event.listens_for(User, 'before_update')
def receive_before_update(mapper, connection, target):
    target.update_level()


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


metadata = MetaData()


class Tier(enum.Enum):
    iron = "iron"
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"
    emerald = "emerald"
    diamond = "diamond"
    master = "master"


class Ranking(Base):
    __tablename__ = "rankings"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    score = Column(Integer)
    tier = Column(SqlEnum(Tier), default=Tier.iron)


class Voca(Base):
    __tablename__ = 'voca'
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    users = relationship(
        'User', secondary=user_voca_association, back_populates='voca_list')
