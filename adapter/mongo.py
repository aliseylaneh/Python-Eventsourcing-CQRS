from pymongo import AsyncMongoClient

from config.mongodb import MongoDBConfig

default_config = MongoDBConfig(
    username="admin",
    password="1234",
    host="localhost",
    port=27017,
    database="inventory",
)

__client = AsyncMongoClient(
    host=default_config.host,
    port=default_config.port,
    username=default_config.username,
    password=default_config.password,
    directconnection=True,
    uuidRepresentation="standard",
)

event_collection = "inventory_events"
outbox_collection = "inventory_outbox"
db = __client[default_config.database]


async def ensure_indexes() -> None:
    await db[event_collection].create_index(
        [("version", 1), ("sku", 1)],
        unique=True,
        name="uniq_sku_version",
    )
    await db[outbox_collection].create_index(
        [("published", 1), ("created_at", 1)],
        name="outbox_unpublished",
    )


async def close_client() -> None:
    await __client.close()
