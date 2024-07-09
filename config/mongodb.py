from dataclasses import dataclass


@dataclass
class MongoDBConfig:
    username: str
    password: str
    host: str
    port: int
    database: str
