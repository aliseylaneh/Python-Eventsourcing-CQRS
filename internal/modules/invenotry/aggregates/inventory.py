from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.modules.invenotry import InventoryEventType, SOHIncreasedEvent, StockReservedEvent


class InventoryAggregate(AggregateRoot):
    inventory: Inventory

    def _when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._handle_reserve_stock_command(event=event)
            case InventoryEventType.SOH_INCREASED:
                self._handle_increase_soh_command(event=event)

    def apply(self, event: Event):
        self._when(event=event)

    def _handle_reserve_stock_command(self, event: StockReservedEvent):
        self.inventory.reserve_stock(event.quantity)
        self.write_repository.reserve(inventory=self.inventory)
        self.event_repository.reserve(inventory=self.inventory)

    def _handle_increase_soh_command(self, event: SOHIncreasedEvent):
        pass
