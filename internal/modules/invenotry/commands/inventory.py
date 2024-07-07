from internal.domain.commands.commands import BaseCommand
from internal.modules.invenotry.events.v1.inventory import StockReservedEvent


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int):
        with self.aggregate:
            event = StockReservedEvent(sku=sku, quantity=quantity)
            self.aggregate.apply(event=event)
