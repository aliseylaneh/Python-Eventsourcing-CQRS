from collections import deque
from uuid import UUID

from src.domain.aggregates.base import AggregateRoot
from src.domain.entities.inventory import Inventory
from src.domain.events.base import Event
from src.domain.exceptions.inventory import (InvalidRelatedEventType,
                                             InventoryDoesNotExists)
from src.modules.invenotry.events.v1.inventory_events import (
    AvailableQuantityDecreasedEvent, AvailableQuantityReplacedEvent,
    BaseInventoryDetailEvent, InventoryCreatedEvent, InventoryEventType,
    ProcessedReservedDecreasedEvent, ProcessedReservedSOHDecreasedEvent,
    ReserveQuantityIncreasedEvent, SOHReplacedEvent)


class InventoryAggregate(AggregateRoot):
    """
    Inventory write-side aggregate.
    It rebuilds Inventory state from events and produces new events for create, reserve, complete and update actions.
    """

    def __init__(self):
        super(InventoryAggregate, self).__init__()
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
        Creates Inventory from InventoryCreatedEvent and if it exists, try to reconstruct the latest state of the inventory.
        Reserved starts from the event reserved value, which is 0 for a newly created inventory.
        :param event:
        :return:
        """

        inventory = Inventory(
            sku=event.sku,
            soh=event.soh,
            available_quantity=event.available_quantity,
            reserved=0,
        )
        self.inventory = inventory

    async def _on_replace_soh(self, event: SOHReplacedEvent):
        """
        Updating and replacing the inventory soh with new value.
        Inventory must already exist, otherwise InventoryDoesNotExists is raised.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.set_soh(soh=event.soh)

    async def _on_replace_available_quantity(
        self, event: AvailableQuantityReplacedEvent
    ):
        """
        Updating and replacing the inventory available quantity with new value.
        :param event:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.set_available_quantity(
            available_quantity=event.available_quantity
        )

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
        When ever we try to decrease a considered amount of reserved
        quantity from an Inventory this handler is initiated by
        ProcessedReservedDecreasedEvent. This handler only decreases reserved.
        Stock on hand is decreased by PROCESSED_RESERVED_SOH_DECREASED in the same complete action.
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

    async def _on_decrease_available_quantity(
        self, event: AvailableQuantityDecreasedEvent
    ):
        """
        Decrease a considered amount of inventory available quantity by event quantity value, decreasing available
        quantity is only initiated when and only by the reserving inventory stock.
        :param event:
        :return:
        """

        if not self.inventory:
            raise InventoryDoesNotExists()
        await self.inventory.update_available_quantity(amount=event.available_quantity)

    async def create(
        self, user_id: UUID, sku: str, soh: int, available_quantity: int
    ) -> deque[Event]:
        """
        Create a new inventory instance and return the events that are generated by this action.
        sku is the string identity of the inventory stream.
        :param sku:
        :param user_id:
        :param soh:
        :param available_quantity:
        :return:
        """
        event = InventoryCreatedEvent(
            user_id=user_id,
            sku=sku,
            soh=soh,
            available_quantity=available_quantity,
            version=self._next_version(),
        )
        await self._on_create_inventory(event=event)
        return deque([event])

    async def reserve_stock(self, user_id: UUID, quantity: int) -> deque[Event]:
        """
        Reserve a considered amount of stock from an inventory and return the events that are generated by this action.
        :param quantity:
        :param user_id:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        reserve_event = ReserveQuantityIncreasedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            reserved=quantity,
            version=self._next_version(),
        )
        available_quantity_event = AvailableQuantityDecreasedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            available_quantity=-quantity,
            version=self._next_version(),
        )
        await self._on_reserve_stock(event=reserve_event)
        await self._on_decrease_available_quantity(event=available_quantity_event)
        return deque([reserve_event, available_quantity_event])

    async def complete_reserved_stock(
        self, user_id: UUID, quantity: int
    ) -> deque[Event]:
        """
        Complete a considered amount of reserved stock from an inventory
        and return the events that are generated by this action.
        It emits PROCESSED_RESERVED_DECREASED with a positive reserved amount
        and PROCESSED_RESERVED_SOH_DECREASED with a negative soh amount.
        :param quantity:
        :param user_id:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()

        decrease_reserved_event = ProcessedReservedDecreasedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            reserved=quantity,
            version=self._next_version(),
        )
        decrease_soh_event = ProcessedReservedSOHDecreasedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            soh=-quantity,
            version=self._next_version(),
        )
        await self._on_decrease_reserved(event=decrease_reserved_event)
        await self._on_decrease_soh(event=decrease_soh_event)
        return deque([decrease_reserved_event, decrease_soh_event])

    async def update(
        self, user_id: UUID, soh: int, available_quantity: int
    ) -> deque[Event]:
        """
        Update a considered amount of inventory soh and available quantity by event soh and available quantity value.
        :param soh:
        :param user_id:
        :param available_quantity:
        :return:
        """
        if not self.inventory:
            raise InventoryDoesNotExists()
        replace_soh_event = SOHReplacedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            soh=soh,
            version=self._next_version(),
        )
        replace_available_quantity_event = AvailableQuantityReplacedEvent(
            user_id=user_id,
            sku=self.inventory.sku,
            available_quantity=available_quantity,
            version=self._next_version(),
        )
        await self._on_replace_soh(event=replace_soh_event)
        await self._on_replace_available_quantity(
            event=replace_available_quantity_event
        )
        return deque([replace_soh_event, replace_available_quantity_event])

    async def apply(self, events: deque[Event]):
        """
        Apply events on aggregate, it's noticeable that an aggregate can
        accept multiple events at the save time and apply them
        to current state of aggregate instance.
        :param events:
        :return:
        """
        for event in events:
            if event.event_type not in InventoryEventType:
                raise InvalidRelatedEventType(
                    event_type=event.event_type, aggregate=InventoryAggregate
                )
        await super(InventoryAggregate, self).apply(events=events)
