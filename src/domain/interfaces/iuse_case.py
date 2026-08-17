from abc import ABC, abstractmethod
from typing import Any


class IUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError
