from internal.modules.invenotry.aggregates.inventory import InventoryAggregate


def inventory_aggregate() -> InventoryAggregate:
    return InventoryAggregate()
