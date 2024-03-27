import os

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

DB_PATH = os.path.abspath('db.db')
engine = create_engine(f'sqlite:////{DB_PATH}', echo=True)
Base = declarative_base()
target_metadata = Base.metadata


class ChoiceScheme(BaseModel):
    id: int | None = None
    text: str
    votes: int
    question_id: int | None = None


class QuestionScheme(BaseModel):
    id: int | None = None
    text: str
    choices: list[ChoiceScheme] | None = None


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(300))
    choices = relationship('Choice', back_populates='question')


class Choice(Base):
    __tablename__ = 'choice'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(300))
    votes = Column(Integer, default=0)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question', back_populates='choices', uselist=False)


def create_database_session() -> Session:
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    session_class = sessionmaker(engine)
    return session_class()


def serialize_choice(choice: Choice) -> ChoiceScheme:
    """ Serialize db choice to pydentic Choice """
    return ChoiceScheme(id=choice.id, text=choice.text, votes=choice.votes, question_id=choice.question_id)


def serialize_question(question: Question) -> QuestionScheme:
    """ Serialize db question to pydentic Question """
    return QuestionScheme(id=question.id, text=question.text,
                          choices=[serialize_choice(choice) for choice in question.choices])
