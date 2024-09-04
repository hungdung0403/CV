from pymongo import MongoClient, errors

from constant.config import USERNAME_DB, PASSWORD_DB, MONGO_URI


def connect_db():
    try:
        db_client = MongoClient(
            host=MONGO_URI,
            serverSelectionTimeoutMS=3000,  # 3 second timeout
            username=str(USERNAME_DB),
            password=str(PASSWORD_DB)
        )
        print('Connected to database.')
    except errors.ServerSelectionTimeoutError as err:
        db_client = None
        print("Server Selection Timeout Error:", err)

    return db_client
