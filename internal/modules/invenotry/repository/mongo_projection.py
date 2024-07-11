from typing import Any

from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory_projection import IInventoryProjection
from internal.modules.invenotry.events.v1.inventory import InventoryEventType, ReserveQuantityIncreasedEvent, \
    AvailableQuantityDecreasedEvent


class MongoProjection(IInventoryProjection):

    def recreate_state(self, events: list[dict], sku: str) -> Inventory:
        # TODO logic is working but must be refactored
        inventory: Inventory = Inventory(sku=sku)
        for event in events:
            match event['event_type']:
                case InventoryEventType.INVENTORY_CREATED:
                    inventory = Inventory(sku=event["sku"],
                                          soh=int(event["soh"]),
                                          available_quantity=int(event['available_quantity']),
                                          reserved=int(event['reserved']))
                case InventoryEventType.STOCK_RESERVED:
                    event: ReserveQuantityIncreasedEvent = event
                    inventory.increase_reserved(int(event['reserved']))
                case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                    event: AvailableQuantityDecreasedEvent = event
                    inventory.update_available_quantity(amount=int(event['available_quantity']))

        return inventory
