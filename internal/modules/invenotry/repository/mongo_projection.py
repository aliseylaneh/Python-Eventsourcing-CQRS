from internal.domain.entities.inventory import Inventory
from internal.domain.interfaces.repositories.iinventory_projection import IInventoryProjection
from internal.modules.invenotry.events.v1.inventory import InventoryEventType


class MongoProjection(IInventoryProjection):

    def recreate_state(self, events: list[dict], sku: str) -> Inventory | None:
        inventory: Inventory = Inventory(sku='')
        for event in events:
            match event['event_type']:
                case InventoryEventType.INVENTORY_CREATED:
                    inventory = Inventory(sku=event["sku"],
                                          soh=int(event["soh"]),
                                          available_quantity=int(event['available_quantity']),
                                          reserved=int(event['reserved']))
                case InventoryEventType.STOCK_RESERVED:
                    inventory.increase_reserved(int(event['reserved']))
                case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                    inventory.update_available_quantity(amount=int(event['available_quantity']))
        if inventory.sku == '':
            return None
        return inventory
