import uuid
from collections import deque

from internal.domain.entities.inventory import Inventory
from internal.domain.events.base import Event
from internal.domain.exceptions.inventory import InventoryDoesNotExists
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.repository.mongo_projection import MongoProjection


class InventoryMongoRepository(IInventoryRepository):
    def create(self, event: Event):
        self._collection.insert(event)

    def bulk_insert(self, events: deque[Event]):
        events = deque(event.__dict__ for event in events)
        self._collection.insert_many(events)

    def find_by_sku(self, sku: str) -> Inventory | None:
        events_sequence = self._collection.find({'sku': sku})
        inventory = MongoProjection().recreate_state(sku=sku, events=events_sequence)
        return inventory

    def find_by_id(self, pk: uuid) -> Inventory:
        pass
