from abc import ABC
from typing import Type

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.iuse_case import IUseCase


class BaseCommand(IUseCase, ABC):
    def __init__(self, aggregate: Type[AggregateRoot]):
        self.aggregate = aggregate
