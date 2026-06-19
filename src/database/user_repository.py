from models import User

from sqlalchemy.orm import Session
from sqlalchemy import select

def get_users_from_db(engine):
    with Session(engine) as session:
        return session.scalars(select(User)).all()

def get_user_from_db(engine, id):
    with Session(engine) as session:
        return session.scalar(select(User).where(User.id == id))
    
def add_user_at_db(engine, user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update_user_at_db(engine, user: User):
    with Session(engine) as session:
        my_user = session.scalar(select(User).where(User.id == user.id))
        if my_user is None:
            return None
        my_user.name = user.name
        my_user.email = user.email
        my_user.password = user.password
        session.commit()
        session.refresh(my_user)
        return my_user

def delete_user_at_db(engine, user: User):
    with Session(engine) as session:
        my_user = session.scalar(select(User).where(User.id == user.id))
        if my_user is None:
            return None
        session.delete(my_user)
        session.commit()
        return my_user