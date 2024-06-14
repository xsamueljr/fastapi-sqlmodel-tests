from sqlmodel import Session

from db.config import engine


def get_session():
    with Session(engine) as session:
        yield session