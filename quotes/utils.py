from pymongo import MongoClient


def get_quotes():
    client = MongoClient('mongodb://localhost')

    db = client.hw_10
    return db
