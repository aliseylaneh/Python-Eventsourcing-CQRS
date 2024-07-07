from pymongo import MongoClient

from config.mongodb import default_config as mongodb_config


def mongo_db_connection(collection: str):
    """
    This handle creating a connection for specific database base on mongodb
    :param collection:
    :return:
    """
    connection_string = f"mongodb+srv://{mongodb_config.username}:{mongodb_config.password}@{mongodb_config.host}/{collection}"
    client = MongoClient(connection_string)
    return client[collection]
