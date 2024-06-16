from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.db.users.db_manager.user import UserDbManager
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetApplicationsResponse(BaseModel):
    calculation_id: str | None
    lot_id: str | None
    client_id: str | None
    shipment_start_date: date | None
    shipment_end_date: date | None
    shipment_volume: int | None
    shipment_address: str | None
    shipment_terms: str | None
    year: int | None
    gar_id: str | None
    spgz_end_id: str | None
    amount: Decimal | None
    unit_of_measurement: str | None
    author_id: UUID | None
    status: str | None
    author_name: str | None
    product_count: int


class GetApplications(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[GetApplicationsResponse]]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            applications = await ApplicationDbManager.get_applications_by_author_id(session, user_id, offset, limit)
            user_ids = {app.author_id for app in applications.objects}

        async with self._main_db_manager.users.make_autobegin_session() as session:
            users = await UserDbManager.get_users_by_ids(session, user_ids)
            user_id_to_name = {user.id: user.name for user in users}

        res = [GetApplicationsResponse(
            calculation_id=app.calculation_id,
            lot_id=app.lot_id,
            client_id=app.client_id,
            shipment_start_date=app.shipment_start_date,
            shipment_end_date=app.shipment_end_date,
            shipment_volume=app.shipment_volume,
            shipment_address=app.shipment_address,
            shipment_terms=app.shipment_terms,
            year=app.year,
            gar_id=app.gar_id,
            spgz_end_id=app.spgz_end_id,
            amount=app.amount,
            unit_of_measurement=app.unit_of_measurement,
            author_id=app.author_id,
            status=app.status,
            author_name=user_id_to_name[app.author_id],
            product_count=len(app.products),
        ) for app in applications.objects]

        return UnifiedResponsePaginated(
            data=DataWithPagination(
                items=res,
                pagination=Pagination(offset=offset, limit=limit, count=applications.count),
            )
        )  # TODO: добавить колво продуктов в заявке
