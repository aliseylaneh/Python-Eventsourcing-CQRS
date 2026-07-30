from collections import deque

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InvalidRelatedEventType, InventoryAlreadyExists, InventoryDoesNotExists
from internal.modules.invenotry.events.v1.inventory import AvailableQuantityDecreasedEvent, AvailableQuantityReplacedEvent, \
    BaseInventoryDetailEvent, InventoryCreatedEvent, InventoryEventType, ProcessedReservedDecreasedEvent, \
    ProcessedReservedSOHDecreasedEvent, ReserveQuantityIncreasedEvent, SOHReplacedEvent


class InventoryAggregate(AggregateRoot):
    def __init__(self, aggregate_id: str):
        super(InventoryAggregate, self).__init__(aggregate_id=aggregate_id)
        self.inventory = None

    async def _when(self, event: Event | BaseInventoryDetailEvent):
        """
        This function will call the specific logic handler depending on the event type of the Event
        :param event:
        :return:
        """
        match event.event_type:
            case InventoryEventType.STOCK_RESERVED:
                await self._on_reserve_stock(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                await self._on_decrease_available_quantity(event=event)
            case InventoryEventType.INVENTORY_CREATED:
                await self._on_create_inventory(event=event)
            case InventoryEventType.SOH_REPLACED:
                await self._on_replace_soh(event=event)
            case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                await self._on_replace_available_quantity(event=event)
            case InventoryEventType.PROCESSED_RESERVED_DECREASED:
                await self._on_decrease_reserved(event=event)
            case InventoryEventType.PROCESSED_RESERVED_SOH_DECREASED:
                await self._on_decrease_soh(event=event)

    async def _on_create_inventory(self, event: InventoryCreatedEvent):
        """
        Creates Inventory and if it exists, try to reconstruct the latest state of the inventory
        :param event:
        :return:
        """

        inventory = Inventory(sku=event.sku, soh=event.soh, available_quantity=event.available_quantity, reserved=0)
        self.inventory = inventory

    async def _on_replace_soh(self, event: SOHReplacedEvent):
        """
        Updating and replacing the inventory soh with new value.
        :param event:
        :return:
        """
        await self.inventory.set_soh(soh=event.soh)

    async def _on_replace_available_quantity(self, event: AvailableQuantityReplacedEvent):
        """
        Updating and replacing the inventory available quantity with new value.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.set_available_quantity(available_quantity=event.available_quantity)

    async def _on_reserve_stock(self, event: ReserveQuantityIncreasedEvent):
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
        await self.inventory.increase_reserved(amount=event.reserved)

    async def _on_decrease_reserved(self, event: ProcessedReservedDecreasedEvent):
        """
        When ever we try to decrease a considered amount of reserved quantity from an Inventory this handler is initiated by
        ProcessedReservedDecreasedEvent. The most important thing is that when we decrease the amount of reserved quantity in
        an Inventory we should decrease the amount of soh too, because that amount is not available to user for reservation.
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.decrease_reserved(amount=event.reserved)

    async def _on_decrease_soh(self, event: ProcessedReservedSOHDecreasedEvent):
        """
        Decrease a considered amount of inventory soh by event soh value, decreasing soh is only initiated
        when and only by the reserved inventory stock.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.update_soh(amount=event.soh)

    async def _on_decrease_available_quantity(self, event: AvailableQuantityDecreasedEvent):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """

        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.update_available_quantity(amount=event.available_quantity)

    async def create(self, sku: int, soh: int, available_quantity: int) -> deque[Event]:
        """
        Create a new inventory instance and return the events that are generated by this action.
        :param sku:
        :param soh:
        :param available_quantity:
        :return:
        """
        event = InventoryCreatedEvent(sku=sku, soh=soh, available_quantity=available_quantity)
        await self._on_create_inventory(event=event)
        return deque([event])

    async def reserve_stock(self, quantity: int) -> deque[Event]:
        """
        Reserve a considered amount of stock from an inventory and return the events that are generated by this action.
        :param quantity:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        reserve_event = ReserveQuantityIncreasedEvent(sku=self.inventory.sku, reserved=quantity)
        available_quantity_event = AvailableQuantityDecreasedEvent(sku=self.inventory.sku, available_quantity=-quantity)
        await self._on_reserve_stock(event=reserve_event)
        await self._on_decrease_available_quantity(event=available_quantity_event)
        return deque([reserve_event, available_quantity_event])

    async def complete_reserved_stock(self, quantity: int) -> deque[Event]:
        """
        Complete a considered amount of reserved stock from an inventory and return the events that are generated by this action.
        :param quantity:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        decrease_reserved_event = ProcessedReservedDecreasedEvent(sku=self.inventory.sku, reserved=quantity)
        decrease_soh_event = ProcessedReservedSOHDecreasedEvent(sku=self.inventory.sku, soh=-quantity)
        await self._on_decrease_reserved(event=decrease_reserved_event)
        await self._on_decrease_soh(event=decrease_soh_event)
        return deque([decrease_reserved_event, decrease_soh_event])

    async def update(self, soh: int, available_quantity: int) -> deque[Event]:
        """
        Update a considered amount of inventory soh and available quantity by event soh and available quantity value.
        :param soh:
        :param available_quantity:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        replace_soh_event = SOHReplacedEvent(sku=self.inventory.sku, soh=soh)
        replace_available_quantity_event = AvailableQuantityReplacedEvent(
            sku=self.inventory.sku,
            available_quantity=available_quantity
        )
        await self._on_replace_soh(event=replace_soh_event)
        await self._on_replace_available_quantity(event=replace_available_quantity_event)
        return deque([replace_soh_event, replace_available_quantity_event])

    async def apply(self, events: deque[Event]):
        """
        Apply events on aggregate, it's noticeable that an aggregate can accept multiple events at the save time and apply them
        to current state of aggregate instance.
        :param events:
        :return:
        """
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(event_type=event.event_type, aggregate=InventoryAggregate)
        await super(InventoryAggregate, self).apply(events=events)
