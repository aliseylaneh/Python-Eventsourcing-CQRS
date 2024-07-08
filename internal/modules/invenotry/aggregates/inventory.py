from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType, OutOfStock
from internal.modules.invenotry.events.v1.inventory import AvailableQuantityDecreasedEvent, InventoryEventType, \
    ReserveQuantityIncreasedEvent


class InventoryAggregate(AggregateRoot):
    inventory: Inventory

    def _when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._on_reserve_stock(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                self._on_decrease_available_quantity(event=event)

    def _get_inventory(self, sku: str):
        if not self.inventory:
            self.inventory = self.repository.find_by_sku(sku=sku)

    def _on_reserve_stock(self, event: Event | ReserveQuantityIncreasedEvent):
        """
        When ever we try to reserve a considered amount of quantity from an Inventory this handler is initiated by
        ReserveQuantityIncreasedEvent. The most important thing is that when we increase the amount of reserve quantity
        in an Inventory we should decrease the amount of Available Quantity too, because that amount is not available
        to user for reservation.
        :param event:
        :return:
        """
        self._get_inventory(sku=event.sku)
        if self.inventory.soh <= 0:
            raise OutOfStock()
        if self.inventory.available_quantity < event.quantity:
            raise OutOfStock()
        self.inventory.reserved += event.quantity
        self.apply(events=deque([AvailableQuantityDecreasedEvent(quantity=event.quantity, sku=event.sku)]))

    def _on_decrease_available_quantity(self, event: Event | AvailableQuantityDecreasedEvent):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """
        self._get_inventory(sku=event.sku)
        self.inventory.available_quantity = event.quantity

    def apply(self, events: deque[Event]):
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(event_type=event.event_type, aggregate=InventoryAggregate)
        super(InventoryAggregate, self).apply(events=events)
