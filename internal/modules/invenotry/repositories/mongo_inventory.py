from collections import deque

import pymongo

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class InventoryMongoRepository(IInventoryRepository):

    async def insert(self, events: deque[Event]):
        events = deque(event.__dict__ for event in events)
        await self._collection.insert_many(events)

    async def find(self, sku: str) -> deque[dict]:
        events_sequence = deque(self._collection.find({'sku': sku}).sort('created_at', pymongo.ASCENDING))
        return events_sequence
