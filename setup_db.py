from app.database import db

if __name__ == "__main__":
    input("This will initialize the database. Press Enter to continue...")
    db.initialize_database()
    print("Database Initialized")