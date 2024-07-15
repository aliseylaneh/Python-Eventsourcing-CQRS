from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType, InventoryAlreadyExists, InventoryDoesNotExists
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.es.services.inventory_utility import MongoDBInventoryUtility
from internal.modules.invenotry.events.v1.inventory import AvailableQuantityDecreasedEvent, AvailableQuantityReplacedEvent, \
    BaseInventoryDetailEvent, InventoryCreatedEvent, InventoryEventType, ProcessedReservedDecreasedEvent, \
    ProcessedReservedSOHDecreasedEvent, ReserveQuantityIncreasedEvent, SOHReplacedEvent


class InventoryAggregate(AggregateRoot):
    def __init__(self, repository: IInventoryRepository):
        super(InventoryAggregate, self).__init__(repository=repository)
        self.inventory = None

    def _when(self, event: Event | BaseInventoryDetailEvent):
        """
        This function will call the specific logic handler depending on the event type of the Event
        :param event:
        :return:
        """
        if not self.inventory:
            self._construct_inventory(sku=event.sku)
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                self._on_reserve_stock(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                self._on_decrease_available_quantity(event=event)
            case InventoryEventType.INVENTORY_CREATED:
                self._on_create_inventory(event=event)
            case InventoryEventType.SOH_REPLACED:
                self._on_replace_soh(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                self._on_replace_available_quantity(event=event)
            case InventoryEventType.PROCESSED_RESERVED_DECREASED:
                self._on_decrease_reserved(event=event)
            case InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED:
                self._on_decrease_soh(event=event)

    def _construct_inventory(self, sku: str):
        """
        Constructing inventory is necessarily for inventory aggregate, so before applying event logics current state
        of aggregate instance must be recreated. This function will call repositories to get the inventory for specific
        sku, and it fulfils the purpose of reconstructing the instance current state.
        :param sku:
        :return:
        """
        if not self.inventory:
            self.inventory = MongoDBInventoryUtility.recreate_state(repository=self.repository, sku=sku)

    def _on_create_inventory(self, event: Event | InventoryCreatedEvent):
        """
        Creates Inventory and if it exists, try to reconstruct the latest state of the inventory
        :param event:
        :return:
        """

        if self.inventory:
            raise InventoryAlreadyExists()
        inventory = Inventory(sku=event.sku, soh=event.soh, available_quantity=event.available_quantity, reserved=0)
        self.inventory = inventory

    def _on_replace_soh(self, event: Event | SOHReplacedEvent):
        """
        Updating and replacing the inventory soh with new value.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.set_soh(soh=event.soh)

    def _on_replace_available_quantity(self, event: Event | AvailableQuantityReplacedEvent):
        """
        Updating and replacing the inventory available quantity with new value.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.set_available_quantity(available_quantity=event.available_quantity)

    def _on_reserve_stock(self, event: Event | ReserveQuantityIncreasedEvent):
        """
        When ever we try to reserve a considered amount of quantity from an Inventory this handler is initiated by
        ReserveQuantityIncreasedEvent. The most important thing is that when we increase the amount of reserve quantity
        in an Inventory we should decrease the amount of Available Quantity too, because that amount is not available
        to user for reservation.
        :param event:
        :return:
        """

        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.increase_reserved(amount=event.reserved)
        self.apply(events=deque([AvailableQuantityDecreasedEvent(sku=event.sku, available_quantity=-event.reserved)]))

    def _on_decrease_reserved(self, event: Event | ProcessedReservedDecreasedEvent):
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.decrease_reserved(amount=event.reserved)
        self.apply(events=deque([ProcessedReservedSOHDecreasedEvent(sku=event.sku, soh=-event.reserved)]))

    def _on_decrease_soh(self, event: Event | ProcessedReservedSOHDecreasedEvent):
        if not self.inventory:
            raise InventoryDoesNotExists()
        self.inventory.update_soh(amount=event.soh)

    def _on_decrease_available_quantity(self, event: Event | AvailableQuantityDecreasedEvent):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """

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
