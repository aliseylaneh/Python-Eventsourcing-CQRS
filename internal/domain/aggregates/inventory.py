import asyncio
from abc import ABC, abstractmethod
from collections import deque

from internal.domain.events.base import Event


class AggregateRoot(ABC):

    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id

    @abstractmethod
    async def _when(self, event: Event):
        raise NotImplementedError


    async def apply(self, events: deque[Event]):
        for event in events:
            await self._when(event=event)
