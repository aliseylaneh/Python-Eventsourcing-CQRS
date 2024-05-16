from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
factory = async_sessionmaker(engine)


def get_db_session() -> AsyncSession:
    session = factory()
    return session
