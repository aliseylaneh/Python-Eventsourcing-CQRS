from abc import abstractmethod, ABC
from typing import Any


class IEventSourcingUtility(ABC):
    @abstractmethod
    async def recreate_state(self, *args, **kwargs) -> Any:
        raise NotImplementedError
