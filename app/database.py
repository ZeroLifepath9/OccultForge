from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    from sqlalchemy import inspect, text

    from app import models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        def _migrate_users(sync_conn):
            insp = inspect(sync_conn)
            if "users" not in insp.get_table_names():
                return
            cols = {c["name"] for c in insp.get_columns("users")}
            if "subscription_tier" not in cols:
                sync_conn.execute(
                    text(
                        "ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(32) DEFAULT 'free'"
                    )
                )
            if "password_hash" not in cols:
                sync_conn.execute(
                    text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)")
                )

        await conn.run_sync(_migrate_users)

        def _migrate_birth_profiles(sync_conn):
            insp = inspect(sync_conn)
            if "birth_profiles" not in insp.get_table_names():
                return
            cols = {c["name"] for c in insp.get_columns("birth_profiles")}
            if "gender" not in cols:
                sync_conn.execute(
                    text(
                        "ALTER TABLE birth_profiles ADD COLUMN gender VARCHAR(16) DEFAULT 'male'"
                    )
                )

        await conn.run_sync(_migrate_birth_profiles)