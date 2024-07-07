import uuid

from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class InventoryMongoRepository(IInventoryRepository):
    def save_events(self, events: list[Event]):
        events = [event.__dict__ for event in events]
        self._events_collection.insert_many(events)

    def create(self, inventory: Inventory) -> Inventory:
        pass

    def update_soh(self, inventory: Inventory) -> Inventory:
        pass

    def reserve(self, inventory: Inventory) -> Inventory:
        pass

    def find_by_id(self, pk: uuid) -> Inventory | None:
        pass

    def find_by_sku(self, sku: str) -> Inventory | None:
        pass
