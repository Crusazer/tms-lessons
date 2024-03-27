import os
from datetime import timezone, timedelta

import sqlalchemy
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

def create_database_session() -> Session:
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    session_class = sessionmaker(engine)
    return session_class()

class Booking(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    date = Column(sqlalchemy.Date, nullable=False)

