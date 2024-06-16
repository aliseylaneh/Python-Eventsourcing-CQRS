from datetime import datetime
import uuid
from dataclasses import dataclass
from enum import Enum


@dataclass
class Event:
    event_id: uuid
    event_type: str
    created_at: datetime.now()


