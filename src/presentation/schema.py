from pydantic import BaseModel

from domain.models import BaseStore, Store


class CreateStore(BaseStore):
    pass


class UpdateStore(Store):
    pass
