from pymongo import MongoClient

from config.mongodb import default_config as mongodb_config


def mongo_db_connection():
    """
    This handle creating a connection for specific database base on mongodb
    :return mongo database:
    """
    connection_string = f"mongodb+srv://{mongodb_config.username}:{mongodb_config.password}@{mongodb_config.host}/{mongodb_config.database}"
    client = MongoClient(connection_string)
    return client
