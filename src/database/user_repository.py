from models import User

from sqlalchemy.orm import Session
from sqlalchemy import select

def get_users(engine):
    with Session(engine) as session:
        return session.scalars(select(User)).all()

def get_user(engine, id):
    with Session(engine) as session:
        return session.scalar(select(User).where(User.id == id))
    
def add_user(engine, user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()

def update_user(engine, user: User):
    with Session(engine) as session:
        my_user = session.scalar(select(User).where(User.id == user.id))
        if my_user is None:
            return None
        my_user.password = user.password
        session.commit()

def delete_user(engine, user: User):
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.id == user.id))
        if user:
            session.delete(user)
            session.commit()