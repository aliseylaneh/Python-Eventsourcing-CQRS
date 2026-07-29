import asyncio
from abc import ABC, abstractmethod
from collections import deque

from internal.domain.events.base import Event


class AggregateRoot(ABC):

    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.events: deque[Event] = deque()

    @abstractmethod
    async def _when(self, event: Event):
        raise NotImplementedError

    async def _apply(self, event):
        await self._when(event=event)
        self.events.append(event)

    async def apply(self, events: deque[Event]):
        await asyncio.gather(*[self._apply(event) for event in events])
