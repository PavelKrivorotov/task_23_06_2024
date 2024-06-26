from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

from main import settings


url = URL.create(
    drivername=settings.DATABASE['DRIVERNAME'],
    username=settings.DATABASE['USER'],
    password=settings.DATABASE['PASSWORD'],
    database=settings.DATABASE['NAME'],
    host=settings.DATABASE['HOST'],
    port=settings.DATABASE['PORT']
)

engine = create_engine(url=url)
session_maker = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=Session
)


def get_db():
    with session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass

