from db import Base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, ForeignKey, DateTime, Time, Float
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer(), primary_key=True)
    text = Column(String())
    first_answer = Column(String())
    second_answer = Column(String(), nullable=True)
    third_answer = Column(String(), nullable=True)
    fourth_answer = Column(String(), nullable=True)
    valid_answer_number = Column(Integer)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    tg_id = Column(BigInteger(), unique=True)
    name = Column(String(), nullable=True)
    is_admin = Column(Boolean(), default=False)
    is_blocked = Column(Boolean(), default=False)


class UserAnswer(Base):
    __tablename__ = "user_answer"
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("user.id"))
    question_id = Column(Integer(), ForeignKey("question.id"))
    user = relationship("User", backref="answers")
    question = relationship("Question", backref="answered_by")
