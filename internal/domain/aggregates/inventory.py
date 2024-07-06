from abc import abstractmethod, ABC

from internal.domain.events.base import Event


class IAggregateRoot(ABC):
    def __init__(self):
        self._events: list[Event] = []
        self._uncommited_events: list[Event] = []

    @abstractmethod
    def apply(self, event: Event):
        pass

    @abstractmethod
    def when(self, event: Event):
        pass
