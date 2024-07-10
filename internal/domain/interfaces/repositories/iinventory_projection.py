from abc import abstractmethod

from internal.domain.events.base import Event


class IInventoryProjection:
    @abstractmethod
    def recreate_state(self, events: list[Event], sku: str):
        raise NotImplementedError
