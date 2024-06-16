from typing import Generic, Sequence, TypeVar

from pydantic.generics import GenericModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def paginated(
    session: AsyncSession, stmt, offset: int, limit: int  # TODO: поднять версии алхимии и использовать Select
) -> Sequence:
    query = await session.execute(stmt.offset(offset).limit(limit))
    return query.scalars().all()


async def count_objects(session: AsyncSession, stmt) -> int:
    stmt = select(func.count()).select_from(stmt.subquery())
    return (await session.execute(stmt)).scalar_one()


T = TypeVar("T")


class ObjectsWithCount(GenericModel, Generic[T]):
    objects: T
    count: int
