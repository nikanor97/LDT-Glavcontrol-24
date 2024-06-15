from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import col

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.forecast import Forecast


class ForecastDbManager(DbManager):
    @staticmethod
    async def get_forecast(
        session: AsyncSession,
        quarter: int | None,
        year: int | None,
        offset: int,
        limit: int,
    ) -> ObjectsWithCount[list[Forecast]]:
        stmt = select(Forecast)
        if quarter is not None:
            stmt = stmt.where(Forecast.quarter == quarter)
        if year is not None:
            stmt = stmt.where(Forecast.year == year)
        stmt = stmt.options(selectinload(Forecast.product))
        forecast = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=forecast, count=count)

    @staticmethod
    async def get_forecast_by_ids(
        session: AsyncSession,
        ids: list[UUID],
    ) -> list[Forecast]:
        stmt = select(Forecast).where(col(Forecast.id).in_(ids))
        forecast = (await session.execute(stmt)).scalars().all()
        return forecast

    @staticmethod
    async def create_forecast(
        session: AsyncSession,
        forecast: Forecast,
    ) -> Forecast:
        forecast = Forecast(**forecast.dict())
        session.add(forecast)
        return forecast
