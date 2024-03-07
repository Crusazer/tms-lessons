import os

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

DB_PATH = os.path.abspath('db.sqlite3')
engine = create_engine(f'sqlite:////{DB_PATH}', echo=True)
Base = declarative_base()
target_metadata = Base.metadata


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

    session_class = sessionmaker(engine)
    return session_class()
