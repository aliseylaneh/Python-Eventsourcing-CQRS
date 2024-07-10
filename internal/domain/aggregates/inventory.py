from abc import ABC, abstractmethod
from collections import deque

from internal.domain.events.base import Event
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class AggregateRoot(ABC):
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    @abstractmethod
    def _when(self, event: Event):
        raise NotImplementedError

    def __enter__(self):
        self.events: deque[Event] = deque()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.events = []
            raise exc_type()

    def commit(self):
        self.repository.bulk_insert(events=self.events)

    def _apply(self, event):
        self._when(event=event)
        self.events.append(event)

    def apply(self, events: deque[Event]):
        for event in events:
            self._apply(event=event)
