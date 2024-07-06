from abc import ABC, abstractmethod

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryCommandRepository


class AggregateRoot(ABC):
    def __init__(self, write_repository: IInventoryCommandRepository, event_repository: IInventoryCommandRepository):
        self.write_repository = write_repository
        self.event_repository = event_repository

    @abstractmethod
    def apply(self, event: Event):
        pass

    @abstractmethod
    def _when(self, event: Event):
        pass