from pydantic import BaseModel, FileUrl


class BaseStore(BaseModel):
    name: str
    address: str
    logo: FileUrl


class Store(BaseStore):
    id: int

    class Config:
        from_attributes = True
