import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


def get_db():
    mongodb_url = os.getenv("Mongo_URL")
    db_name = os.getenv("db_name")
    print("db",db_name)
    print("db",mongodb_url)

    client = pymongo.MongoClient(mongodb_url)
    database = client[db_name]
    return database

