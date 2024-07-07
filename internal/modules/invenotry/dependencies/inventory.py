from fastapi import Depends

from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from pkg.mongodb.mongodb import mongo_db_connection


def get_inventory_collection():
    mongo_db_connection(collection='inventory')


def get_event_collection():
    return mongo_db_connection(collection='inventory_events')


def inventory_repository(inventory_collection=Depends(get_inventory_collection),
                         events_collection=Depends(get_event_collection)) -> IInventoryRepository:
    return IInventoryRepository(collection=inventory_collection, events_collection=events_collection)


def inventory_aggregate(repository=Depends(inventory_repository)) -> InventoryAggregate:
    return InventoryAggregate(repository=repository)
