import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class BaseTimeStamp(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field()


class Store(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    address: str
