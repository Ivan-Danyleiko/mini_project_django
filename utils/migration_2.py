import os
import django
from dateutil import parser

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fine_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient("mongodb://localhost")
db = client.hw_10
authors = db.authors.find()

for author_data in authors:
    born_date_str = author_data.get("born_date", "")
    if born_date_str:
        born_date = parser.parse(born_date_str).strftime('%Y-%m-%d')
        author = Author.objects.filter(fullname=author_data['fullname']).first()
        if not author:
            author = Author.objects.create(
                fullname=author_data['fullname'],
                born_date=born_date,
                born_location=author_data['born_location'],
                description=author_data['description'],
            )

quotes = db.quotes.find()

for quote_data in quotes:
    tags = []
    for tag in quote_data['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exit_quote = bool(len(Quote.objects.filter(quote=quote_data["quote"])))

    if not exit_quote:
        author = db.authors.find_one({'_id': quote_data['author']})
        a = Author.objects.filter(fullname=author['fullname']).first()
        if not a:
            born_date = parser.parse(author.get('born_date', '')).strftime('%Y-%m-%d')
            a = Author.objects.create(
                fullname=author['fullname'],
                born_date=born_date,
                born_location=author['born_location'],
                description=author['description'],
            )
        q = Quote.objects.create(
            quote=quote_data["quote"],
            author=a,
        )
        for tag in tags:
            q.tags.add(tag)
