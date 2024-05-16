from pydantic import BaseModel


class BaseStore(BaseModel):
    name: str
    address: str
    logo: bytes | None


class Store(BaseStore):
    id: int

    class Config:
        from_attributes = True
