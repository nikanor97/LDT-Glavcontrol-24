from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.application_product import ApplicationProductDbManager
from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.company import Company
from src.db.projects.models.product import Product
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class UpdateApplicationWithProductsRequestProduct(BaseModel):
    id: UUID | None  # если None, то продукт надо создать
    name: str | None
    price: Decimal | None
    number: int | None
    amount: Decimal | None


class UpdateApplicationWithProductsRequest(BaseModel):
    id: UUID
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
    status: str | None  # draft | ready

    products: list[UpdateApplicationWithProductsRequestProduct]


class UpdateApplicationWithProductsResponseProduct(BaseModel):
    id: UUID
    name: str | None
    price: Decimal | None
    number: int | None
    amount: Decimal | None


class UpdateApplicationWithProductsResponse(BaseModel):
    id: UUID
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
    status: str | None  # draft | ready
    # author_id: UUID
    created_at: datetime
    updated_at: datetime
    products: list[UpdateApplicationWithProductsResponseProduct]


class UpdateApplicationWithProducts(ProjectsEndpoints):
    async def call(
        self,
        data: UpdateApplicationWithProductsRequest,
    ) -> UnifiedResponse[UpdateApplicationWithProductsResponse]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:

            application = Application(**data.dict(exclude={"products"}))
            new_application = await ApplicationDbManager.update_application(
                session, application
            )

            # products = [Product(**p.dict()) for p in data.products]

            # print(f"{products=}")

            products_to_create = [Product(**p.dict()) for p in data.products if p.id is None]
            new_products = await ProductDbManager.create_products(session, products_to_create)

            await session.flush()

            products_to_update = [Product(**p.dict()) for p in data.products if p.id is not None]
            updated_products = await ProductDbManager.update_products(session, products_to_update)

            await session.flush()

            application_products = await ApplicationProductDbManager.update_application_products(
                session, application.id, [p.id for p in new_products + updated_products]
            )

            await session.flush()

            updated_application = await ApplicationDbManager.get_application(session, application.id)
            # print(updated_application)
            res = UpdateApplicationWithProductsResponse(
                **updated_application.dict(),
                products=[UpdateApplicationWithProductsResponseProduct(
                    **upd_ap.dict()
                ) for upd_ap in updated_application.products]
            )

        return UnifiedResponse(data=res)

