from abc import ABC

from internal.domain.interfaces.iuse_case import IUseCase
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class BaseQuery(IUseCase, ABC):
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository
