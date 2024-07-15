from internal.domain.entities.inventory import Inventory
from internal.domain.interfaces.ies_utility import IEventSourcingUtility
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.events.v1.inventory import InventoryEventType


class MongoDBInventoryUtility(IEventSourcingUtility):
    @staticmethod
    def recreate_state(repository: IInventoryRepository, sku: str) -> Inventory | None:
        events = repository.find(sku=sku)
        inventory: Inventory = Inventory(sku='')
        for event in events:
            match event.get('event_type'):
                case InventoryEventType.INVENTORY_CREATED:
                    inventory = Inventory(sku=event.get('sku'),
                                          soh=int(event.get('soh')),
                                          available_quantity=int(event.get('available_quantity')),
                                          reserved=int(event.get('reserved')))
                case InventoryEventType.STOCK_RESERVED:
                    inventory.increase_reserved(int(event.get('reserved')))
                case InventoryEventType.AVAILABLE_QUANTITY_DECREASED:
                    inventory.update_available_quantity(amount=int(event.get('available_quantity')))
                case InventoryEventType.AVAILABLE_QUANTITY_REPLACED:
                    inventory.set_available_quantity(available_quantity=int(event.get('available_quantity')))
                case InventoryEventType.SOH_REPLACED:
                    inventory.set_soh(soh=int(event.get('soh')))
        if inventory.sku == '':
            return None
        return inventory
