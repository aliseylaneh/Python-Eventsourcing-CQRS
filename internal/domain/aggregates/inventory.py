from abc import ABC, abstractmethod

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class AggregateRoot(ABC):
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    @abstractmethod
    def apply(self, event: Event):
        pass

    @abstractmethod
    def _when(self, event: Event):
        pass
