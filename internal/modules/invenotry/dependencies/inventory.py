from fastapi import Depends

from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate


def inventory_aggregate(repository=Depends(IInventoryRepository)) -> InventoryAggregate:
    return InventoryAggregate(repository=repository)
