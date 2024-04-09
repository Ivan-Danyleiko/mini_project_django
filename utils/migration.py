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

for author in authors:
    born_date_str = author.get("born_date", "")
    if born_date_str:
        born_date = parser.parse(born_date_str).strftime('%Y-%m-%d')
        Author.objects.get_or_create(
            fullname=author.get("fullname", ""),
            born_date=born_date,
            born_location=author.get("born_location", ""),
            description=author.get("description", ""),
        )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exit_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))

    if not exit_quote:
        author = db.authors.find_one({'_id': quote['author']})
        born_date_str = author.get("born_date", "")
        if born_date_str:
            born_date = parser.parse(born_date_str).strftime('%Y-%m-%d')
        a, _ = Author.objects.get_or_create(
            fullname=author.get("fullname", ""),
            defaults={
                'born_date': born_date,
                'born_location': author.get("born_location", ""),
                'description': author.get("description", "")
            }
        )
        q = Quote.objects.create(
            quote=quote["quote"],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)
