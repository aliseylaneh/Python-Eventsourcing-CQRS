from collections import deque

from ..events.v1.inventory import ReserveQuantityIncreasedEvent
from ....domain.commands.commands import BaseCommand


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int):
        with self.aggregate:
            self.aggregate.apply(events=deque([ReserveQuantityIncreasedEvent(sku=sku, quantity=quantity)]))
