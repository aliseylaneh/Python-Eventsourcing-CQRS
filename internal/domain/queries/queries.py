from abc import ABC

from internal.domain.interfaces.iuse_case import IUseCase


class BaseQuery(IUseCase, ABC):
    def __init__(self):
        pass
