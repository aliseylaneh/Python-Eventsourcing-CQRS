from pymongo import MongoClient

from config.mongodb import MongoDBConfig

default_config = MongoDBConfig(username='admin',
                               password='1234',
                               host='localhost',
                               port=27017,
                               database='inventory')


def mongo_db_connection():
    """
    This handle creating a connection for specific database base on mongodb
    :return mongo database:
    """
    connection_string = f"mongodb://{default_config.username}:{default_config.password}@{default_config.host}/{default_config.database}"
    client = MongoClient(connection_string)
    return client['inventory']
