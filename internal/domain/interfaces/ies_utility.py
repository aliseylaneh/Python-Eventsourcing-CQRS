from abc import abstractmethod
from typing import Any


class IEventSourcingUtility:
    @abstractmethod
    def recreate_state(self, *args, **kwargs) -> Any:
        raise NotImplementedError
