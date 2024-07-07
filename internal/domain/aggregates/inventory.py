from abc import ABC, abstractmethod

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class AggregateRoot(ABC):
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    @abstractmethod
    def _when(self, event: Event):
        raise NotImplementedError

    def __enter__(self):
        self.events: list[Event] = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.events = []

    def commit(self):
        self.repository.save_events(event=self.events)

    def _apply(self, event: Event):
        self._when(event)
        self.events.append(event)

    def apply(self, event: Event):
        self._apply(event=event)
