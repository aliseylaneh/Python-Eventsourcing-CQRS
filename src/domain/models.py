from pydantic import BaseModel


class BaseStore(BaseModel):
    name: str
    address: str


class Store(BaseStore):
    id: int

    class Config:
        orm_mode = True
