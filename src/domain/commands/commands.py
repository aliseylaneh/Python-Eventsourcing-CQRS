from abc import ABC

from src.domain.interfaces.iuse_case import IUseCase
from src.domain.interfaces.repositories.iinventory import \
    IMongoInventoryWriteRepository


class BaseCommand(IUseCase, ABC):
    def __init__(self, event_repository: IMongoInventoryWriteRepository):
        self.event_repository = event_repository
