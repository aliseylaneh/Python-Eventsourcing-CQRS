import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class Event:
    version: int
    event_id: UUID = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: UUID
    event_type: Enum = None
    occurred_at: datetime = field(default_factory=datetime.now)
