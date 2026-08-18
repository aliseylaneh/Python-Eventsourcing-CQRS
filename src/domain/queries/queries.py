from abc import ABC

from src.domain.interfaces.iuse_case import IUseCase
from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryReadRepository


class BaseQuery(IUseCase, ABC):
    def __init__(self, repository: IMongoInventoryReadRepository):
        self._repository = repository
