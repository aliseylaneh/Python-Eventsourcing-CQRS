from fastapi import Depends

from internal.modules.invenotry.aggregates.inventory import InventoryAggregate
from internal.modules.invenotry.repository.elasticsearch_inventory import InventoryElasticSearchCommandRepository


def inventory_aggregate(event_repo=Depends(InventoryElasticSearchCommandRepository),
                        write_repo=Depends(InventoryElasticSearchCommandRepository)) -> InventoryAggregate:
    return InventoryAggregate(write_repository=write_repo, event_repository=event_repo)
