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