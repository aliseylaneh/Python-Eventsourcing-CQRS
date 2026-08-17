from abc import ABC
from typing import Type

from src.domain.aggregates.base import AggregateRoot
from src.domain.interfaces.iuse_case import IUseCase
from src.domain.interfaces.repositories.iinventory import \
    IInventoryRepository


class BaseCommand(IUseCase, ABC):
    def __init__(
        self, aggregate: Type[AggregateRoot], event_repository: IInventoryRepository
    ):
        self.aggregate = aggregate
        self.event_repository = event_repository
