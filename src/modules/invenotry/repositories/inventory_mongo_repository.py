from collections import deque
from copy import deepcopy
from enum import Enum
from typing import Any, Dict
from uuid import UUID

import pymongo
from pymongo.asynchronous.database import AsyncDatabase

from config.otel import tracer
from src.domain.events.base import Event
from src.domain.interfaces.repositories.iinventory import (
    IMongoInventoryReadRepository,
    IMongoInventoryWriteRepository,
)
from src.modules.invenotry.events.v1.inventory_events import (
    InventoryEventDTO,
    InventoryEventType,
)

INVENTORY_PROJECTION_COLLECTION = "inventory_projections"


def _event_to_document(event: Event) -> dict[str, Any]:
    """
    Convert a domain event to a Mongo document.
    Enum event_type is stored as its string value so it can be loaded later.
    :param event: domain event
    :return: serializable event document
    """
    document = dict(event.__dict__)
    event_type = document.get("event_type")
    if isinstance(event_type, Enum):
        document["event_type"] = event_type.value
    return document


def _document_to_event(document: dict[str, Any]) -> InventoryEventDTO:
    """
    Convert a stored event or outbox document to InventoryEventDTO.
    Mongo and outbox bookkeeping fields are removed before reconstructing the DTO.
    :param document: raw Mongo document
    :return: common inventory event DTO used by aggregate replay and projection
    """
    payload = dict(document)
    payload.pop("_id", None)
    payload.pop("published", None)
    payload.pop("created_at", None)
    event_type = payload.get("event_type")
    if event_type is not None and not isinstance(event_type, InventoryEventType):
        payload["event_type"] = InventoryEventType(event_type)
    return InventoryEventDTO(**payload)


class InventoryWriteRepository(IMongoInventoryWriteRepository):
    """
    Mongo implementation of the inventory event store and transactional outbox.
    """

    def __init__(self, db: AsyncDatabase, event_collection: str, outbox_collection: str):
        super(InventoryWriteRepository, self).__init__(
            db=db,
            event_collection=event_collection,
            outbox_collection=outbox_collection,
        )

    async def insert(self, events: deque[Event]):
        """
        Insert sequence of events into event collection and also outbox collection.
        Both writes happen in one Mongo transaction. Outbox copies start as unpublished
        so the projection worker can apply them to the read model later.
        :param events: sequence of events
        """
        event_documents = [_event_to_document(event) for event in events]
        outbox_documents = [
            {
                **deepcopy(document),
                "published": False,
                "created_at": document.get("occurred_at"),
            }
            for document in event_documents
        ]
        async with self._db.client.start_session() as session:
            async with await session.start_transaction():
                await self._db[self._event_collection].insert_many(
                    event_documents, session=session, ordered=True
                )
                await self._db[self._outbox_collection].insert_many(
                    outbox_documents, session=session, ordered=True
                )

    async def find(self, sku: str) -> deque[InventoryEventDTO]:
        """
        Find events based on sku and reflect the retrieved data into common DTO.
        Events are sorted by version so aggregate replay stays in the same order they were written.
        :param sku: sku
        :return: deque[InventoryEventDTO]
        """

        events_sequence = (
            await self._db[self._event_collection]
            .find(
                {"sku": sku},
                {
                    "_id": 0,
                },
            )
            .sort("version", pymongo.ASCENDING)
            .to_list(length=None)
        )
        if len(events_sequence) != 0:
            return deque(_document_to_event(event) for event in events_sequence)
        return deque(events_sequence)

    async def find_unpublished(self) -> deque[InventoryEventDTO]:
        """
        Find unpublished outbox events ordered by created_at for the projection worker.
        :return: deque[InventoryEventDTO]
        """
        unpublished = (
            await self._db[self._outbox_collection]
            .find({"published": False})
            .sort("created_at", pymongo.ASCENDING)
            .to_list(length=None)
        )
        return deque(_document_to_event(event) for event in unpublished)

    async def mark_published(self, event_id: UUID | str) -> None:
        """
        Mark an unpublished outbox event as published after it was projected.
        :param event_id: identity of the event in the outbox
        :return:
        """
        await self._db[self._outbox_collection].update_one(
            {"event_id": event_id, "published": False},
            {"$set": {"published": True}},
        )


class InventoryReadRepository(IMongoInventoryReadRepository):
    """
    Mongo implementation of the inventory read model / projection store.
    Mutation methods only apply an event when last_applied_version is lower than the incoming version.
    """

    def __init__(self, db: AsyncDatabase, projection_store: str):
        super(InventoryReadRepository, self).__init__(
            db=db, projection_collection=projection_store
        )

    async def create(self, inventory: Dict[str, Any]) -> None:
        """
        Create new inventory projection if a document with the same sku does not exist.
        Replay of INVENTORY_CREATED does not overwrite an already projected inventory.
        :param inventory: inventory
        """
        await self._db[self._projection_collection].update_one(
            {"sku": inventory["sku"]},
            {"$setOnInsert": inventory},
            upsert=True,
        )

    async def find(self, sku: str) -> Dict[str, Any] | None:
        """
        Find a single inventory based on sku.
        Internal projection fields such as _id and last_applied_version are not returned to queries.
        :param sku: sku
        :return: projected inventory or None
        """
        with tracer.start_as_current_span(f"get-{sku}-repository-find"):
            result = await self._db[self._projection_collection].find_one(
                {"sku": sku},
                {"_id": 0, "last_applied_version": 0},
            )
            return result

    async def set_soh(self, sku: str, soh: int, version: int) -> None:
        """
        Replace projected soh when event version is newer than last_applied_version.
        :param sku: sku
        :param soh: new stock on hand
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {"$set": {"soh": soh, "last_applied_version": version}},
        )

    async def set_available_quantity(
            self, sku: str, available_quantity: int, version: int
    ) -> None:
        """
        Replace projected available quantity when event version is newer than last_applied_version.
        :param sku: sku
        :param available_quantity: new available quantity
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {
                "$set": {
                    "available_quantity": available_quantity,
                    "last_applied_version": version,
                },
            },
        )

    async def increase_reserved(self, sku: str, amount: int, version: int) -> None:
        """
        Increase projected reserved quantity when event version is newer than last_applied_version.
        :param sku: sku
        :param amount: reserved delta
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {
                "$inc": {"reserved": amount},
                "$set": {"last_applied_version": version},
            },
        )

    async def decrease_reserved(self, sku: str, amount: int, version: int) -> None:
        """
        Decrease projected reserved quantity when event version is newer than last_applied_version.
        Amount is a positive reserved value, so the document is incremented by the negative amount.
        :param sku: sku
        :param amount: positive reserved amount that should be subtracted
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {
                "$inc": {"reserved": -amount},
                "$set": {"last_applied_version": version},
            },
        )

    async def decrease_available_quantity(
            self, sku: str, amount: int, version: int
    ) -> None:
        """
        Apply a signed available quantity delta when event version is newer than last_applied_version.
        Reserve events pass a negative amount, so available quantity decreases.
        :param sku: sku
        :param amount: signed available quantity delta
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {
                "$inc": {"available_quantity": amount},
                "$set": {"last_applied_version": version},
            },
        )

    async def decrease_soh(
            self,
            sku: str,
            amount: int,
            version: int,
    ) -> None:
        """
        Apply a signed soh delta when event version is newer than last_applied_version.
        Completing reserved stock passes a negative amount, so soh decreases.
        :param sku: sku
        :param amount: signed soh delta
        :param version: event version
        :return:
        """
        await self._db[self._projection_collection].update_one(
            {"sku": sku, "last_applied_version": {"$lt": version}},
            {
                "$inc": {"soh": amount},
                "$set": {"last_applied_version": version},
            },
        )
