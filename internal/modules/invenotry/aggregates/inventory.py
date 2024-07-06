from internal.domain.aggregates.inventory import IAggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.events.v1.inventory import InventoryEventType, StockReservedEvent, SOHIncreasedEvent


class InventoryAggregate(IAggregateRoot):

    def __init__(self):
        super(InventoryAggregate, self).__init__()
        self.inventory: Inventory = None

    def when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._on_reserve_stock(event=event)
            case InventoryEventType.SOH_INCREASED:
                self._on_increase_soh(event=event)

    def apply(self, event: Event):
        self.when(event=event)

    def _get_inventory(self, pk: int):
        pass

    def _on_reserve_stock(self, event: StockReservedEvent):
        self.inventory.reserve(event.quantity)

    def _on_increase_soh(self, event: SOHIncreasedEvent):
        pass
