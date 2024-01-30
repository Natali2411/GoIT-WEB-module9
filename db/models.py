import logging
import sys
from typing import List

from mongoengine import *
import redis
from redis_lru import RedisLRU


logging.basicConfig()
logger = logging.getLogger("mongo")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class Author(Document):
    fullname = StringField(max_length=200, required=True, unique=True)
    born_date = DateTimeField(required=True)
    born_location = StringField(max_length=300, required=True)
    description = StringField(max_length=10000, required=True)

    meta = {"db_alias": "goid-db-alias"}


class Tag(EmbeddedDocument):
    name = StringField(max_length=100, required=True)

    meta = {"db_alias": "goid-db-alias"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(max_length=500, required=True)
    tags = ListField(EmbeddedDocumentField(Tag))

    meta = {"db_alias": "goid-db-alias"}


class ManipulateData:
    client = redis.StrictRedis(host="localhost", port=6379, password=None)
    cache = RedisLRU(client)

    @staticmethod
    def transform_query_data(quotes: List[Quote]) -> List[dict]:
        return [
            {
                "author": quote.author.fullname,
                "quote": quote.quote,
                "tags": [tag.name for tag in quote.tags],
            }
            for quote in quotes
        ]

    @staticmethod
    @cache
    def get_quotes_by_name(author_name: str):
        logger.info("Get quotes by author name")
        author = Author.objects(fullname=author_name).first()
        quotes = Quote.objects(author=author)
        return ManipulateData.transform_query_data(quotes=quotes)

    @staticmethod
    @cache
    def get_quotes_by_tags(*args):
        logger.info("Get quotes by tags")
        quotes = Quote.objects(tags__name__in=args)
        return ManipulateData.transform_query_data(quotes=quotes)
