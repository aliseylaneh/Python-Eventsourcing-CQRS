from abc import ABC

from internal.domain.aggregates.inventory import AggregateRoot
from internal.domain.interfaces.iuse_case import IUseCase


class BaseCommand(IUseCase, ABC):
    def __init__(self, aggregate: AggregateRoot):
        self.aggregate = aggregate
