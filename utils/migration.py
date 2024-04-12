import os
import django
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fine_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author

client = MongoClient("mongodb://localhost")
db = client.hw_10

authors = db.authors.find()

for author in authors:
    fullname = author.get("fullname", "")
    if fullname:
        if not Author.objects.filter(fullname=fullname).exists():
            born_date_str = author.get("born_date", "")
            born_date = datetime.strptime(born_date_str, "%B %d, %Y").date() if born_date_str else None
            Author.objects.create(
                fullname=fullname,
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
        author = Author.objects.filter(fullname=quote['author']).first()
        if author:
            q = Quote.objects.create(
                quote=quote["quote"],
                author=author
            )
            for tag in tags:
                q.tags.add(tag)
