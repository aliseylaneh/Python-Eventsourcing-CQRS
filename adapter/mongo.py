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

    client = MongoClient(host=default_config.host,
                         port=default_config.port,
                         username=default_config.username,
                         password=default_config.password)
    return client['inventory']
