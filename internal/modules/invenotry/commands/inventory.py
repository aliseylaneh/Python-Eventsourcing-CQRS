from fastapi import Depends

from internal.domain.events.v1.inventory import StockReservedEvent
from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.dependencies import inventory_aggregate


class ReserveStockCommand:
    def __init__(self):
        self.aggregate = InventoryAggregate()

    def execute(self, sku: str, quantity: int, aggregate: Depends(InventoryAggregate)):
        self.aggregate.apply(event=StockReservedEvent(sku=sku, quantity=quantity))
