from abc import ABC
from typing import Type

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.iuse_case import IUseCase
from internal.domain.interfaces.repositories.iinventory import IInventoryRepository


class BaseCommand(IUseCase, ABC):
    def __init__(self, aggregate: Type[AggregateRoot],
                 event_repository: IInventoryRepository):
        self.aggregate = aggregate
        self.event_repository = event_repository
