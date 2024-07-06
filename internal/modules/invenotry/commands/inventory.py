from internal.domain.commands.commands import BaseCommand
from internal.modules.invenotry.events.v1.inventory import StockReservedEvent


class ReserveStockCommand(BaseCommand):
    def execute(self, sku: str, quantity: int):
        self.aggregate.apply(event=StockReservedEvent(sku=sku, quantity=quantity))
