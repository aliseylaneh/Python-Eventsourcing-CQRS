from infrastructure.settings.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
