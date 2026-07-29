from pymongo.asynchronous.mongo_client import AsyncMongoClient

from config.mongodb import MongoDBConfig

default_config = MongoDBConfig(username='admin',
                               password='1234',
                               host='localhost',
                               port=27017,
                               database='inventory')

__client = AsyncMongoClient(host=default_config.host,
                            port=default_config.port,
                            username=default_config.username,
                            password=default_config.password)
db = __client['inventory']
