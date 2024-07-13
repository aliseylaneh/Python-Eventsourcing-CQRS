from fastapi import Depends

from adapter.mongo import mongo_db_connection
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.commands.inventory import CreateInventoryCommand, ReserveStockCommand, UpdateInventoryCommand
from internal.modules.invenotry.repository.mongo_inventory import InventoryMongoRepository


def get_inventory_collection():
    return mongo_db_connection()['inventory']


def inventory_repository(collection=Depends(get_inventory_collection)) -> IInventoryRepository:
    return InventoryMongoRepository(collection=collection)


def inventory_aggregate(repository=Depends(inventory_repository)) -> InventoryAggregate:
    return InventoryAggregate(repository=repository)


def get_reserve_stock_command(aggregate=Depends(inventory_aggregate)) -> ReserveStockCommand:
    return ReserveStockCommand(aggregate=aggregate)


def get_create_inventory_command(aggregate=Depends(inventory_aggregate)) -> CreateInventoryCommand:
    return CreateInventoryCommand(aggregate=aggregate)


def get_update_inventory_command(aggregate=Depends(inventory_aggregate)) -> UpdateInventoryCommand:
    return UpdateInventoryCommand(aggregate=aggregate)
