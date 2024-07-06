from internal.domain.aggregates.inventory import IAggregateRoot


class BaseCommand:
    def __init__(self, aggregate: IAggregateRoot):
        self.aggregate = aggregate
