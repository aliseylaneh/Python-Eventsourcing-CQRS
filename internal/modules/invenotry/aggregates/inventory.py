from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.modules.invenotry.events.v1.inventory import InventoryEventType, StockReservedEvent, SOHIncreasedEvent


class InventoryAggregate(AggregateRoot):
    inventory: Inventory

    def _when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._handle_reserve_stock(event=event)
            case InventoryEventType.SOH_INCREASED:
                self._handle_increase_soh(event=event)

    def apply(self, event: Event):
        self._when(event=event)

    def _handle_reserve_stock(self, event: StockReservedEvent):
        self.inventory = self.repository.find_by_sku(sku=event.sku)
        self.inventory.reserve_stock(event.quantity)
        self.repository.reserve(inventory=self.inventory)

    def _handle_increase_soh(self, event: SOHIncreasedEvent):
        pass
