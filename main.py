from database import engine, add_users
from user import Base

# Création des tables
if __name__ == "__main__":
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    add_users()
    print("Tables créées avec succès !")