from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from loguru import logger
from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.application_product import ApplicationProductDbManager
from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.application_product import ApplicationProduct
from src.db.projects.models.product import Product
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class CreateApplicationRequestProduct(BaseModel):
    name: str | None
    price: Decimal | None
    number: int | None
    amount: Decimal | None


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

    products: list[CreateApplicationRequestProduct]


class CreateApplicationResponse(BaseModel):
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
    created_at: date
    updated_at: date
    products: list[Product]


class CreateApplication(ProjectsEndpoints):
    async def call(
        self,
        data: CreateApplicationRequest,
        token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UnifiedResponse[CreateApplicationResponse]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            application = Application(**data.dict(exclude={"products"}), author_id=user_id, status="draft")
            new_application = await ApplicationDbManager.create_application(
                session, application
            )

            await session.flush()

            products = [Product(
                name=product.name,
                price=product.price,
                number=product.number,
                amount=product.amount,
            ) for product in data.products]
            new_products = await ProductDbManager.create_products(session, products)

            await session.flush()

            application_products = [ApplicationProduct(
                application_id=application.id,
                product_id=product.id
            ) for product in new_products]
            new_application_products = await ApplicationProductDbManager.create_application_products(
                session, application_products
            )

            created_application = await ApplicationDbManager.get_application(session, new_application.id)
            res = CreateApplicationResponse(**created_application.dict(), products=created_application.products)

        return UnifiedResponse(data=res)

