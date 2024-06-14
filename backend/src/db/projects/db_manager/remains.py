from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import col

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.remains import Remains


class RemainsDbManager(DbManager):
    @staticmethod
    async def get_remains_for_period(
        session: AsyncSession,
        start_date: date,
        end_date: date,
    ) -> list[Remains]:
        stmt = select(Remains).where(
            (Remains.date >= start_date) & (Remains.date <= end_date)
        )
        remains = (await session.execute(stmt)).scalars().all()
        return remains

    @staticmethod
    async def get_remains(
        session: AsyncSession,
        offset: int,
        limit: int,
    ) -> ObjectsWithCount[list[Remains]]:
        stmt = select(Remains)
        remains = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=remains, count=count)

    @staticmethod
    async def get_remains_by_ids(
        session: AsyncSession,
        ids: list[UUID],
    ) -> list[Remains]:
        stmt = select(Remains).where(col(Remains.id).in_(ids))
        remains = (await session.execute(stmt)).scalars().all()
        return remains

    @staticmethod
    async def create_remains(
        session: AsyncSession,
        remains: Remains,
    ) -> Remains:
        session.add(remains)
        return remains
