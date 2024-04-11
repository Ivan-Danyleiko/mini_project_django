import os
import django
from django.utils.dateparse import parse_date
from datetime import datetime
from bson import ObjectId

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fine_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient("mongodb://localhost")
db = client.hw_10

authors = db.authors.find()

for author in authors:
    author_id = str(author['_id'])
    if not Author.objects.filter(id=author_id).exists():
        born_date_str = author.get("born_date", "")
        if born_date_str:
            born_date = parse_date(datetime.strptime(born_date_str, "%B %d, %Y").strftime('%Y-%m-%d'))
        else:
            born_date = None
        fullname = author.get("fullname", "")
        if fullname:
            a, created = Author.objects.get_or_create(
                id=author_id,
                fullname=fullname,
                born_date=born_date,
                born_location=author.get("born_location", ""),
                description=author.get("description", ""),
            )

quotes = db.quotes.find()

for quote in quotes:
    author_id = str(quote['author'])
    if not Author.objects.filter(id=author_id).exists():
        author = Author.objects.get(id=author_id)
        tags = []
        for tag_name in quote['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        q = Quote.objects.create(
            quote=quote["quote"],
            author=author
        )
        q.tags.add(*tags)
