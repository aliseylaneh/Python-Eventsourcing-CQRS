from typing import Annotated

from pydantic import BaseModel, Base64Bytes, EncodedBytes, Base64Encoder, FileUrl


class BaseStore(BaseModel):
    name: str
    address: str
    logo: FileUrl


class Store(BaseStore):
    id: int

    class Config:
        from_attributes = True
