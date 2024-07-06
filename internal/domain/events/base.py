from datetime import datetime
import uuid
from dataclasses import dataclass
from enum import Enum


@dataclass
class Event:
    event_id: uuid
    event_type: str
    created_at: datetime

    def __init__(self):
        self.event_id = str(uuid.uuid4())
        self.created_at = datetime.now()
