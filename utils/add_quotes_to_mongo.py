import json
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost")

db = client.hw_10

with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({'fullname': quote['author']})
    if not author:
        author_id = db.authors.insert_one({'fullname': quote['author']}).inserted_id
    else:
        author_id = author['_id']

    db.quotes.insert_one({
        'quote': quote['quote'],
        'tags': quote['tags'],
        'author': quote['author'],
    })
