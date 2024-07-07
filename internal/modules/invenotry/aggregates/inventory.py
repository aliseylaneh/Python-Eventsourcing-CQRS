from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType
from internal.modules.invenotry.events.v1.inventory import InventoryEventType, ReserveQuantityIncreasedEvent


class InventoryAggregate(AggregateRoot):
    inventory: Inventory

    def _when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._handle_reserve_stock(event=event)

    def _init_inventory(self, sku: str):
        if not self.inventory:
            self.inventory = self.repository.find_by_sku(sku=sku)

    def _handle_reserve_stock(self, event: Event | ReserveQuantityIncreasedEvent):
        self._init_inventory(sku=event.sku)
        new_available_quantity = self.inventory.reserve_stock(event.quantity)
        self.

    def _handle_
    def apply(self, events: deque[Event]):
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(event_type=event.event_type, aggregate=InventoryAggregate)
        super(InventoryAggregate, self).apply(events=events)
