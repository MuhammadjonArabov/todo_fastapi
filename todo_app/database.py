from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Asynchronous engine
SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_host}/{settings.db_name}'
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# Synchronous engine for schema creation
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL.replace('+asyncpg', ''))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
