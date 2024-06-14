from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class CreateApplicationRequest(BaseModel):
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


class CreateApplication(ProjectsEndpoints):
    async def call(
        self,
        data: CreateApplicationRequest,
    ) -> UnifiedResponse[Application]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            application = Application(**data.dict())
            new_application = await ApplicationDbManager.create_application(
                session, application
            )
        return UnifiedResponse(data=new_application)

