from datetime import datetime

import mongoengine

from db_connect import connect_mongo_db
from file_utils import FileInteraction
from models import Author, Quote, Tag


def write_to_db(authors_file_path: str, quotes_file_path: str) -> None:
    # Add authors
    authors_file_objects = FileInteraction.read_info(authors_file_path)
    quotes_file_objects = FileInteraction.read_info(quotes_file_path)
    for instance in authors_file_objects:
        row_data = instance
        born_date: datetime = datetime.strptime(row_data["born_date"], "%B %d, %Y")
        born_date_fmt: str = datetime.strftime(born_date, "%Y-%m-%d")
        row_data["born_date"] = born_date_fmt
        author = Author(**row_data)
        try:
            author.save()
        except mongoengine.errors.NotUniqueError:
            print(
                f"The author with the name '{author.fullname}' already "
                f"exist in the collection"
            )

    # Add quotes
    for instance in quotes_file_objects:
        row_data = instance
        author = Author.objects(fullname=row_data["author"])[0]
        if author:
            row_data["author"] = author
            row_data["tags"] = [Tag(name=tag_name) for tag_name in row_data["tags"]]
            quote = Quote(**row_data)
            quote.save()


if __name__ == "__main__":
    connect_mongo_db()
    write_to_db("data/authors.json", "data/quotes.json")
