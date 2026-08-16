from collections import deque
from typing import Any, Deque

import pymongo
from pymongo.asynchronous.database import AsyncDatabase

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import \
    IInventoryRepository
from internal.modules.invenotry.events.v1.inventory import InventoryEventDTO


class InventoryMongoRepository(IInventoryRepository):
    def __init__(self, db: AsyncDatabase, event_store: str, outbox_store: str):
        super(InventoryMongoRepository, self).__init__(
            db=db, event_store=event_store, outbox_store=outbox_store
        )

    async def insert(self, events: deque[Event]):
        events_collection: Deque[dict[str, Any]] = deque()
        outbox_collection: Deque[dict[str, Any]] = deque()

        for event in events:
            event_doc = event.__dict__
            outbox_doc = {
                "event": event_doc,
                "created_at": event.occurred_at,
                "published": False,
            }
            events_collection.append(event_doc)
            outbox_collection.append(outbox_doc)

        async with self._db.client.start_session() as session:
            async with await session.start_transaction():
                await self._db[self._event_store].insert_many(
                    events_collection, session=session, ordered=True
                )
                await self._db[self._outbox_store].insert_many(
                    outbox_collection, session=session
                )

    async def find(self, sku: str) -> deque[dict]:
        events_sequence = (
            await self._db[self._event_store]
            .find(
                {"sku": sku},
                {
                    "_id": 0,
                },
            )
            .sort("occurred_at", pymongo.ASCENDING)
            .to_list(length=None)
        )
        if len(events_sequence) != 0:
            result = deque([InventoryEventDTO(**event) for event in events_sequence])
            return result
        return deque(events_sequence)
