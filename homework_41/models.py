import os.path

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

DB_PATH = os.path.abspath('db.sqlite3')
engine = create_engine(f'sqlite:////{DB_PATH}')
Base = declarative_base()
target_metadata = Base.metadata


def create_database_session() -> Session:
    if not database_exists(engine.url):
        create_database(engine.url)

    session_class = sessionmaker(engine)
    return session_class()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), default='')
    last_name = Column(String(30), default='')
    email = Column(String(50))
    username = Column(String(30))
    password = Column(String(50))


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    description = Column(String(500))
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='products', uselist=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    products = relationship('Product', back_populates='category')
