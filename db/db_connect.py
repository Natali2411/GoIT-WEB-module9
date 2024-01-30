import os

from mongoengine import connect

from read_config import get_conf_value

mongo_user = get_conf_value("DB", "user")
mongodb_pass = get_conf_value("DB", "pass")
db_name = get_conf_value("DB", "db_name")
domain = get_conf_value("DB", "domain")


def connect_mongo_db():
    # is_local_connect = os.environ.get("IS_LOCAL", False)
    is_local_connect = True
    if is_local_connect:
        return connect(host="localhost", port=27017, alias="goid-db-alias", db="goit")
    else:
        return connect(
            host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""",
            ssl=True,
            alias="goid-db-alias",
        )


if __name__ == "__main__":
    connect_mongo_db()

# mongodb://localhost:27017
