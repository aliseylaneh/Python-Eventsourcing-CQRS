import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


@dataclass
class Event:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: Enum = None
    created_at: datetime = field(default_factory=datetime.now)
