from database import Base, engine, SessionLocal
from user import User

# Créer les tables
def create_tables():
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

# Ajouter des utilisateurs
def add_users():
    session = SessionLocal()
    try:
        user1 = User(name="Alice", age=25)
        user2 = User(name="Bob", age=30)
        session.add_all([user1, user2])
        session.commit()
        print("Utilisateurs ajoutés avec succès !")
    finally:
        session.close()

# Lire tous les utilisateurs
def get_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Age: {user.age}")
    finally:
        session.close()

# Mettre à jour un utilisateur
def update_user(user_id, new_name):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.name = new_name
            session.commit()
            print(f"Utilisateur {user_id} mis à jour avec succès !")
        else:
            print(f"Aucun utilisateur trouvé avec l'ID {user_id}")
    finally:
        session.close()

# Supprimer un utilisateur
def delete_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            session.delete(user)
            session.commit()
            print(f"Utilisateur {user_id} supprimé avec succès !")
        else:
            print(f"Aucun utilisateur trouvé avec l'ID {user_id}")
    finally:
        session.close()

# Menu principal
def main():
    print("Options disponibles :")
    print("1 : Créer les tables")
    print("2 : Ajouter des utilisateurs")
    print("3 : Lire les utilisateurs")
    print("4 : Mettre à jour un utilisateur")
    print("5 : Supprimer un utilisateur")

    choice = input("Entrez le numéro de l'opération : ")
    match choice:
        case "1":
            create_tables()
        case "2":
            add_users()
        case "3":
            get_users()
        case "4":
            user_id = int(input("ID de l'utilisateur à mettre à jour : "))
            new_name = input("Nouveau nom : ")
            update_user(user_id, new_name)
        case "5":
            user_id = int(input("ID de l'utilisateur à supprimer : "))
            delete_user(user_id)
        case "exit":
            exit()
        case _:
            print("Choix invalide.")



if __name__ == "__main__":
    while True:
        main()

