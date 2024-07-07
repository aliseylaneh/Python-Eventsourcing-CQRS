from dataclasses import dataclass


@dataclass
class MongoDBConfig:
    username: str
    password: str
    host: str
    port: int
    database: str


default_config = MongoDBConfig(username='admin',
                               password='m@1234',
                               host='localhost',
                               port=27017,
                               database='inventory')
