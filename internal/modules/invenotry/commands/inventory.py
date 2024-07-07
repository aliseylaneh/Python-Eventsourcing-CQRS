from collections import deque

from internal.domain.commands.commands import BaseCommand
from internal.modules.invenotry.events.v1.inventory import ReserveQuantityIncreasedEvent


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int):
        with self.aggregate:
            reserve_stock = deque()
            reserve_stock.append(ReserveQuantityIncreasedEvent(sku=sku, quantity=quantity))
            self.aggregate.apply(events=reserve_stock)
