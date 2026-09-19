from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Dict
from uuid import UUID

from pymongo.asynchronous.database import AsyncDatabase

from src.domain.events.base import Event


class IMongoInventoryWriteRepository(ABC):
    """
    Write-side inventory repository contract.
    It persists domain events in the event store and unpublished copies in the outbox.
    """

    def __init__(self, db, event_collection, outbox_collection):
        self._db: AsyncDatabase = db
        self._event_collection = event_collection
        self._outbox_collection = outbox_collection

    @abstractmethod
    async def insert(self, events: deque[Event]):
        """
        Insert sequence of events into event collection and also outbox collection.
        :param events: sequence of events
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def find(self, sku: str) -> deque[Event]:
        """
        Load the ordered event stream of a sku so the aggregate can rebuild its state.
        :param sku: sku
        :return: ordered events of the inventory
        """
        raise NotImplementedError

    @abstractmethod
    async def find_unpublished(self) -> deque[Event]:
        """
        Load outbox events that are not projected yet, ordered by created_at.
        :return: unpublished outbox events
        """
        raise NotImplementedError

    @abstractmethod
    async def mark_published(self, event_id: UUID | str) -> None:
        """
        Mark a single outbox event as published after it was projected into the read model.
        :param event_id: identity of the event in the outbox
        :return:
        """
        raise NotImplementedError


class IMongoInventoryReadRepository(ABC):
    """
    Read-side inventory repository contract.
    It stores the denormalized projection used by queries.
    """

    def __init__(self, db: AsyncDatabase, projection_collection: str):
        self._db: AsyncDatabase = db
        self._projection_collection = projection_collection

    @abstractmethod
    async def create(self, inventory: Dict[str, Any]) -> None:
        """
        Create new inventory projection if it does not exist.
        :param inventory: inventory
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def find(self, sku: str) -> Dict[str, Any] | None:
        """
        Find a single inventory projection based on sku.
        :param sku: sku
        :return: projected inventory or None when it is not projected yet
        """
        raise NotImplementedError

    @abstractmethod
    async def set_soh(self, sku: str, soh: int, version: int) -> None:
        """
        Replace projected soh when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param soh: new stock on hand
        :param version: event version
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def set_available_quantity(
        self,
        sku: str,
        available_quantity: int,
        version: int,
    ) -> None:
        """
        Replace projected available quantity when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param available_quantity: new available quantity
        :param version: event version
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def increase_reserved(self, sku: str, amount: int, version: int) -> None:
        """
        Increase projected reserved quantity when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param amount: reserved delta
        :param version: event version
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def decrease_reserved(self, sku: str, amount: int, version: int) -> None:
        """
        Decrease projected reserved quantity when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param amount: positive reserved amount that should be subtracted
        :param version: event version
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def decrease_soh(self, sku: str, amount: int, version: int) -> None:
        """
        Apply a signed soh delta on the projection when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param amount: signed soh delta
        :param version: event version
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def decrease_available_quantity(
        self, sku: str, amount: int, version: int
    ) -> None:
        """
        Apply a signed available quantity delta when the incoming event version is newer than last_applied_version.
        :param sku: sku
        :param amount: signed available quantity delta
        :param version: event version
        :return:
        """
        raise NotImplementedError
