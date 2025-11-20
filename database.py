from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from user import User

DATABASE_URL = "sqlite:///utilisateurs.db"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def  add_users():
    db_session = SessionLocal()
    try:
        user1 = User(name="Alex", age=21)
        user2 = User(name="Bruno", age=22)
        db_session.add_all([user1, user2])
        db_session.commit()
        print("Utilisateurs Ajoutés !")
    finally:
        db_session.close()