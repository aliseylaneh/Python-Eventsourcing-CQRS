from collections import deque

import pymongo

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository
from internal.modules.invenotry.events.v1.inventory import InventoryEventDTO


class InventoryMongoRepository(IInventoryRepository):

    async def insert(self, events: deque[Event]):
        events = deque(event.__dict__ for event in events)
        await self._collection.insert_many(events)

    async def find(self, sku: str) -> deque[dict]:
        events_sequence = await self._collection.find(
            {
                'sku': sku
            },
            {
                "_id": 0,
            }
        ).sort(
            'created_at', pymongo.ASCENDING).to_list(length=None)
        if len(events_sequence) != 0:
            result = deque([InventoryEventDTO(**event) for event in events_sequence])
            return result
        return deque(events_sequence)
