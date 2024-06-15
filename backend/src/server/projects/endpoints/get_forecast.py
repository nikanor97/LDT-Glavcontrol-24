from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.models.forecast import Forecast
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetForcastResponseProduct(BaseModel):
    name: str | None
    price: Decimal | None
    number: int | None
    amount: Decimal | None


class GetForcastResponse(BaseModel):
    product_id: UUID | None
    quarter: int | None
    year: int | None
    product: GetForcastResponseProduct | None


class GetForecast(ProjectsEndpoints):

    async def call(
        self,
        quarter: int | None = None,
        year: int | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Forecast]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            forecast = await ForecastDbManager.get_forecast(session, quarter, year, offset, limit)

            res: list[GetForcastResponse] = []
            for idx, forc in enumerate(forecast.objects):
                res.append(GetForcastResponse(
                    product_id=forc.product_id,
                    quarter=forc.quarter,
                    year=forc.year,
                    product=GetForcastResponseProduct(
                        name=forc.product.name,
                        price=forc.product.price,
                        number=forc.product.number,
                        amount=forc.product.amount,
                    )
                ))
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=res,
                    pagination=Pagination(offset=offset, limit=limit, count=forecast.count),
                )
            )
