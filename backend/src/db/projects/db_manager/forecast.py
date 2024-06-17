import json
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import col

import settings
from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.models.forecast import Forecast
from src.db.projects.models.product import Product


class ForecastDbManager(DbManager):
    @staticmethod
    async def get_forecast(
        session: AsyncSession,
        company_id: UUID,
        quarter: int | None,
        year: int | None,
        offset: int,
        limit: int,
    ) -> ObjectsWithCount[list[Forecast]]:
        stmt = select(Forecast).where(Forecast.company_id == company_id)
        if quarter is not None:
            stmt = stmt.where(Forecast.quarter == quarter)
        if year is not None:
            stmt = stmt.where(Forecast.year == year)
        stmt = stmt.options(selectinload(Forecast.product), selectinload(Forecast.company))
        forecast = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=forecast, count=count)

    @staticmethod
    async def get_all_forecast(
        session: AsyncSession,
        company_id: UUID,
        quarter: int | None,
        year: int | None,
    ) -> list[Forecast]:
        stmt = select(Forecast).where(Forecast.company_id == company_id)
        if quarter is not None:
            stmt = stmt.where(Forecast.quarter == quarter)
        if year is not None:
            stmt = stmt.where(Forecast.year == year)
        stmt = stmt.options(selectinload(Forecast.product), selectinload(Forecast.company))
        forecast = (await session.execute(stmt)).scalars().all()
        return forecast

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

    @staticmethod
    async def create_forecast_from_recom(
        session: AsyncSession,
        company_id: UUID,
    ) -> None:
        with open(f'{settings.BASE_DIR}/date/рекомендации.json', 'r') as f:
            recom = json.load(f)

        products = [Product(
            name=r['name'],
            price=r['Цена ГК, руб.'],
            number=1,
            amount=r['Цена ГК, руб.'],
        ) for r in recom]

        forecast = [Forecast(
            product_id=product.id,
            quarter=1,
            year=2023,
            company_id=company_id
        ) for product in products]

        await ProductDbManager.create_products(session, products)
        for f in forecast:
            await ForecastDbManager.create_forecast(session, f)
