from abc import ABC, abstractmethod
from collections import deque

from src.domain.events.base import Event


class AggregateRoot(ABC):
    """
    Base class for event sourced aggregates.
    It keeps the current version of the aggregate and applies events in order
    so the in-memory state can be rebuilt from the event stream.
    """

    def __init__(self):
        self.version: int = 0

    @abstractmethod
    async def _when(self, event: Event):
        """
        Route a single event to the matching state handler in the concrete aggregate.
        :param event: domain event that should mutate aggregate state
        :return:
        """
        raise NotImplementedError

    async def apply(self, events: deque[Event]):
        """
        Replay a sequence of events on the aggregate and set version to the last applied event.
        :param events: ordered events that belong to this aggregate
        :return:
        """
        for event in events:
            await self._when(event=event)
            self.version = event.version

    def _next_version(self):
        """
        Increase aggregate version by one and return the next version for a newly created event.
        :return: next event version
        """
        self.version += 1
        return self.version
