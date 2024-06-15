from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.product import Product
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination, UnifiedResponse
from src.server.projects import ProjectsEndpoints


class GetApplicationResponse(BaseModel):
    id: UUID
    calculation_id: str | None
    lot_id: str | None
    client_id: str | None
    shipment_start_date: date
    shipment_end_date: date
    shipment_volume: int | None
    shipment_address: str | None
    shipment_terms: str | None
    year: int | None
    gar_id: str | None
    spgz_end_id: str | None
    amount: Decimal | None
    unit_of_measurement: str | None
    status: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime
    products: list[Product]


class GetApplication(ProjectsEndpoints):

    async def call(
        self,
        application_id: UUID,
    ) -> UnifiedResponse[GetApplicationResponse]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            application = await ApplicationDbManager.get_application(session, application_id)
            res = GetApplicationResponse(**application.dict(), products=application.products)
        return UnifiedResponse(data=res)
