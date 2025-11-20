from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Création de la base SQLite
engine = create_engine("sqlite:///example.db")
Base = declarative_base()

# Exemple de modèle
class User(Base):
    __tablename__ = "users_exemples"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# Création des tables
Base.metadata.create_all(engine)

# Session
Session = sessionmaker(bind=engine)
session = Session()

print("Base de données SQLite prête !")