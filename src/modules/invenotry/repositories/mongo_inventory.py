from collections import deque
from typing import Any, Deque

import pymongo
from pymongo.asynchronous.database import AsyncDatabase

from src.domain.events.base import Event
from src.domain.interfaces.repositories.iinventory import \
    IInventoryRepository, IInventoryProjectionRepository
from src.modules.invenotry.events.v1.inventory import InventoryEventDTO


class InventoryMongoRepository(IInventoryRepository):
    def __init__(self, db: AsyncDatabase, event_store: str):
        super(InventoryMongoRepository, self).__init__(db=db, event_store=event_store)

    async def insert(self, events: deque[Event]):
        """
        Insert sequence of events into event collection and also outbox collection.
        :param events: sequence of events
        """
        events_collection: Deque[dict[str, Any]] = deque(
            event.__dict__ for event in events
        )
        async with self._db.client.start_session() as session:
            async with await session.start_transaction():
                await self._db[self._event_store].insert_many(
                    events_collection, session=session, ordered=True
                )

    async def find(self, sku: str) -> deque[dict]:
        """
        Find events based on sku and reflect the retrieved data into common DTO.
        :param sku: sku
        :return: deque[dict]
        """
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


class InventoryMongoProjectionRepository(IInventoryProjectionRepository):

    async def decrease_reserved_and_soh(self, sku: str, amount: int) -> None:
        pass

    def __init__(self, db):
        self.collection = db["inventory_read_model"]

    async def create(self, inventory: dict[str, Any]) -> None:
        await self.collection.insert_one(inventory)

    async def replace_soh(
            self,
            sku: str,
            soh: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$set": {
                    "soh": soh,
                }
            },
        )

    async def replace_available_quantity(
            self,
            sku: str,
            available_quantity: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$set": {
                    "available_quantity": available_quantity,
                }
            },
        )

    async def increase_reserved(
            self,
            sku: str,
            amount: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$inc": {
                    "reserved": amount,
                },
            },
        )

    async def decrease_reserved(
            self,
            sku: str,
            amount: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$inc": {
                    "reserved": amount,
                }
            },
        )

    async def decrease_available_quantity(
            self,
            sku: str,
            amount: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$inc": {
                    "available_quantity": amount,
                }
            },
        )

    async def decrease_soh(
            self,
            sku: str,
            amount: int,
    ) -> None:
        await self.collection.update_one(
            {"sku": sku},
            {
                "$inc": {
                    "soh": amount,
                }
            },
        )
