from domain.models import BaseStore, Store


class CreateStore(BaseStore):
    logo: bytes


class UpdateStore(Store):
    pass
