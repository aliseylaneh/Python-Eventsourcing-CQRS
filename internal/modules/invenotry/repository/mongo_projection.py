from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory_projection import IInventoryProjection
from internal.modules.invenotry.events.v1.inventory import InventoryEventType, ReserveQuantityIncreasedEvent, \
    AvailableQuantityDecreasedEvent


class MongoProjection(IInventoryProjection):

    def recreate_state(self, events: list[Event], sku: str) -> Inventory:
        # TODO
        inventory: Inventory = Inventory(sku=sku)
        for event in events:
            match event.event_type:
                case InventoryEventType.STOCK_RESERVED:
                    event: ReserveQuantityIncreasedEvent = event
                    inventory.increase_reserved(event.reserved)
                case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                    event: AvailableQuantityDecreasedEvent = event
                    inventory.decrease_available_quantity(event.available_quantity)

        return inventory
