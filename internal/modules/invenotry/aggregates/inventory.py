from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType, OutOfStock, QuantityError
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.events.v1.inventory import AvailableQuantityDecreasedEvent, InventoryEventType, \
    ReserveQuantityIncreasedEvent


class InventoryAggregate(AggregateRoot):
    def __init__(self, repository: IInventoryRepository):
        super(InventoryAggregate, self).__init__(repository=repository)
        self.inventory = None

    def _when(self, event: Event):
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._on_reserve_stock(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                self._on_decrease_available_quantity(event=event)

    def _construct_inventory(self, sku: str):
        self.inventory = Inventory(sku=sku, soh=100, available_quantity=60, reserved=0)
        # if not self.inventory:
        #     self.inventory = self.repository.find_by_sku(sku=sku)

    def _on_reserve_stock(self, event: Event | ReserveQuantityIncreasedEvent):
        """
        When ever we try to reserve a considered amount of quantity from an Inventory this handler is initiated by
        ReserveQuantityIncreasedEvent. The most important thing is that when we increase the amount of reserve quantity
        in an Inventory we should decrease the amount of Available Quantity too, because that amount is not available
        to user for reservation.
        :param event:
        :return:
        """
        self._construct_inventory(sku=event.sku)
        self.inventory.increase_reserved(amount=event.reserved)
        self.apply(events=deque([AvailableQuantityDecreasedEvent(available_quantity=event.reserved, sku=event.sku)]))

    def _on_decrease_available_quantity(self, event: Event | AvailableQuantityDecreasedEvent):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """
        self._construct_inventory(sku=event.sku)
        self.inventory.decrease_available_quantity(amount=event.available_quantity)

    def apply(self, events: deque[Event]):
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(event_type=event.event_type, aggregate=InventoryAggregate)
        super(InventoryAggregate, self).apply(events=events)
