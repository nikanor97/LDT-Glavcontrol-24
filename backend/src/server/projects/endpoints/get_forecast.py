from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.forecast import Forecast
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetForcastResponseProduct(BaseModel):
    name: str | None
    price: Decimal | None
    number: int | None
    amount: Decimal | None
    type: str | None
    # cluster: int | None
    description: str | None


class GetForcastResponse(BaseModel):
    id: UUID
    product_id: UUID | None
    quarter: int | None
    year: int | None
    product: GetForcastResponseProduct | None


class GetForecast(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        quarter: int | None = None,
        year: int | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Forecast]]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)

            procurements = await ProcurementDbManager.get_procurements(
                session, user_company.company_id, offset=0, limit=1
            )
            if procurements.count == 0:
                return UnifiedResponsePaginated(
                    data=DataWithPagination(
                        items=[],
                        pagination=Pagination(offset=offset, limit=limit, count=0),
                    )
                )
            else:
                forecast = await ForecastDbManager.get_forecast(
                    session, user_company.company_id, quarter, year, offset, limit
                )

                res: list[GetForcastResponse] = []
                for idx, forc in enumerate(forecast.objects):
                    res.append(GetForcastResponse(
                        id=forc.id,
                        product_id=forc.product_id,
                        quarter=forc.quarter,
                        year=forc.year,
                        product=GetForcastResponseProduct(
                            name=forc.product.name,
                            price=forc.product.price,
                            number=forc.product.number,
                            amount=forc.product.amount,
                            type=forc.product.type,
                            description=forc.product.description
                        )
                    ))
                return UnifiedResponsePaginated(
                    data=DataWithPagination(
                        items=res,
                        pagination=Pagination(offset=offset, limit=limit, count=forecast.count),
                    )
                )
