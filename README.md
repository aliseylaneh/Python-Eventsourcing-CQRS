Python-Eventsourcing-CQRS

This project is a Python-based implementation of **Domain-Driven Design (DDD)**, **Event Sourcing**, and **CQRS (Command Query Responsibility Segregation)** using the FastAPI framework. It showcases the use of repository and aggregate patterns, emphasizing modularity, scalability, and clean architecture principles.

## Features
- **Domain-Driven Design (DDD):** Clear separation of concerns between domain, application, and infrastructure layers.
- **Event Sourcing:** Persistence of domain events instead of current state, enabling robust historical tracking and debugging.
- **CQRS:** Segregation of commands (write operations) and queries (read operations) for better scalability and performance.
- **Repository Pattern:** Abstracts data storage implementation.
- **Aggregate Pattern:** Ensures domain integrity and consistency.

---

## Directory Structure
```plaintext
└── aliseylaneh-Python-Eventsourcing-CQRS/
    ├── README.md
    ├── docker-compose.dev.yml
    ├── docker-compose.yml
    ├── main.py
    ├── pyproject.toml
    ├── adapter/
    ├── config/
    ├── docker/
    ├── internal/            # Domain logic and core business rules
    │   ├── domain/          # DDD Aggregates, Commands, Entities, Events, Exceptions
    │   ├── es/              # Event sourcing utilities and services
    │   └── modules/         # Use-case and layer implementations
    └── ...
```

### Key Components
1. **Domain Layer (`internal/domain/`):**
   - Aggregates: Encapsulates business logic and ensures consistency.
   - Commands: Represents domain commands (write operations).
   - Entities: Core business objects.
   - Events: Domain events for event sourcing.
   - Exceptions: Custom exceptions for domain logic.
   - Interfaces: Defines contracts (e.g., repositories, use cases).

2. **Event Sourcing (`internal/es/`):**
   - Reconstructs the current state by replaying domain events.

3. **Modules Layer (`internal/modules/`):**
   - Implements use cases and integrates domain logic with infrastructure.

4. **Adapters (`adapter/`):**
   - Infrastructure-related implementations (e.g., MongoDB adapters).

5. **Configuration (`config/`):**
   - Configuration utilities (e.g., MongoDB, OpenTelemetry).

---

## Running the Project

### Prerequisites
- Docker and Docker Compose

### Steps
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd aliseylaneh-Python-Eventsourcing-CQRS
   ```

2. **Start the infrastructure using Docker Compose:**
   ```bash
   docker-compose up -d
   ```
   This starts the following services:
   - MongoDB: Database for event persistence.
   - Mongo-Express: MongoDB web UI (accessible at `http://localhost:8081`).
   - Elasticsearch: Used for logging and tracing.
   - Jaeger: Distributed tracing (accessible at `http://localhost:16686`).

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```
   The FastAPI application will be available at `http://localhost:8000`.

---

## Example Domain Implementation

### Aggregate Root Example
```python
class AggregateRoot(ABC):
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def commit(self):
        self.repository.insert(events=self.events)

    def _apply(self, event):
        self._when(event=event)
        self.events.append(event)
```

### Inventory Entity Example
```python
@dataclass
class Inventory:
    sku: str = field(default='')
    soh: int = field(default=0)
    available_quantity: int = field(default=0)
    reserved: int = field(default=0)

    def set_soh(self, soh: int):
        if self.reserved >= soh:
            raise ReservedStockInProcess()
        self.soh = soh
```

### Event Sourcing Utility Example
```python
class MongoDBInventoryUtility(IEventSourcingUtility):
    @staticmethod
    def recreate_state(repository: IInventoryRepository, sku: str) -> Inventory | None:
        events = repository.find(sku=sku)
        inventory = Inventory(sku='')
        for event in events:
            # Process events to recreate state
            ...
        return inventory
```

---

## Configuration

### MongoDB
MongoDB is used as the primary event store. The default connection details are:
- Host: `localhost`
- Port: `27017`
- Database: `inventory`
- Username: `admin`
- Password: `1234`

### Distributed Tracing
- Jaeger is used for distributed tracing.
- Access the Jaeger UI at `http://localhost:16686`.

---

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact
For questions or support, please open an issue or reach out to the repository owner.

