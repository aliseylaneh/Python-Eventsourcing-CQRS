from abc import ABC, abstractmethod
from collections import deque

from internal.domain.events.base import Event


class AggregateRoot(ABC):

    def __init__(self):
        self.version: str = 0

    @abstractmethod
    async def _when(self, event: Event):
        raise NotImplementedError

    async def apply(self, events: deque[Event]):
        for event in events:
            await self._when(event=event)
            self.version = event.version

    def _next_version(self):
        self.version += 1
        return self.version
