from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType, InventoryAlreadyExists, InventoryDoesNotExists
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.events.v1.inventory import AvailableQuantityDecreasedEvent, InventoryCreatedEvent, InventoryEventType, \
    ReserveQuantityIncreasedEvent


class InventoryAggregate(AggregateRoot):
    def __init__(self, repository: IInventoryRepository):
        super(InventoryAggregate, self).__init__(repository=repository)
        self.inventory = None

    def _when(self, event: Event):
        """
        This function will call the specific logic handler depending on the event type of the Event
        :param event:
        :return:
        """
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._on_reserve_stock(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                self._on_decrease_available_quantity(event=event)
            case InventoryEventType.INVENTORY_CREATED:
                self._on_create_inventory(event=event)

    def _construct_inventory(self, sku: str):
        """
        Constructing inventory is necessarily for inventory aggregate, so before applying event logics current state of aggregate
        instance must be recreated. This function will call repository to get the inventory for specific sku, and it fulfils the
        purpose of reconstructing the instance current state.
        :param sku:
        :return:
        """
        if not self.inventory:
            self.inventory = self.repository.find_by_sku(sku=sku)

    def _on_create_inventory(self, event: Event | InventoryCreatedEvent):
        """
        Creates Inventory and if it exists, try to reconstruct the latest state of inventory then triggers below events:
        1- IncreasedSohQuantityEvent
        2- IncreasedAvailableQuantityEvent
        :param event:
        :return:
        """
        self._construct_inventory(sku=event.sku)
        if self.inventory:
            raise InventoryAlreadyExists()
        inventory = Inventory(sku=event.sku, soh=event.soh, available_quantity=event.available_quantity, reserved=0)
        self.inventory = inventory

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
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.increase_reserved(amount=event.reserved)
        self.apply(events=deque([AvailableQuantityDecreasedEvent(available_quantity=-event.reserved, sku=event.sku)]))

    def _on_decrease_available_quantity(self, event: Event | AvailableQuantityDecreasedEvent):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """
        self._construct_inventory(sku=event.sku)
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.update_available_quantity(amount=event.available_quantity)

    def apply(self, events: deque[Event]):
        """
        Apply events on aggregate, it's noticeable that an aggregate can accept multiple events at the save time and apply them
        to current state of aggregate instance.
        :param events:
        :return:
        """
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(event_type=event.event_type, aggregate=InventoryAggregate)
        super(InventoryAggregate, self).apply(events=events)
