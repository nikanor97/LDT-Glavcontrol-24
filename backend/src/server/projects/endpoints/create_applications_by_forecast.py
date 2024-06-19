from collections import defaultdict
from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from loguru import logger
from pydantic import BaseModel

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.application_product import ApplicationProductDbManager
from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.application_product import ApplicationProduct
from src.db.projects.models.product import Product
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class CreateApplicationsFromForecastRequest(BaseModel):
    forecast_ids: list[UUID]


class CreateApplicationsFromForecastResponse(BaseModel):
    application_ids: list[UUID]


class CreateApplicationsFromForecast(ProjectsEndpoints):
    async def call(
        self,
        data: CreateApplicationsFromForecastRequest,
        token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UnifiedResponse[CreateApplicationsFromForecastResponse]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            forecast_items = await ForecastDbManager.get_forecast_by_ids(session, data.forecast_ids)
            cluster_to_products: defaultdict[int, list[Product]] = defaultdict(list)
            for forecast_item in forecast_items:
                cluster_to_products[forecast_item.product.cluster].append(forecast_item.product)

            applications: list[Application] = []
            application_products: list[ApplicationProduct] = []
            for cluster, products in cluster_to_products.items():
                application = Application(
                    calculation_id=None,
                    lot_id=None,
                    client_id=None,
                    shipment_start_date=None,
                    shipment_end_date=None,
                    shipment_volume=None,
                    shipment_address=None,
                    shipment_terms=None,
                    year=None,
                    gar_id=None,
                    spgz_end_id=None,
                    amount=None,
                    unit_of_measurement=None,
                    author_id=user_id,
                    status="draft"
                )
                applications.append(application)
                application_product_items = [ApplicationProduct(
                    application_id=application.id,
                    product_id=product.id
                ) for product in products]
                application_products.extend(application_product_items)

            new_applications = await ApplicationDbManager.create_applications(
                session, applications
            )
            await session.flush()
            new_application_products = await ApplicationProductDbManager.create_application_products(
                session, application_products
            )

            res = CreateApplicationsFromForecastResponse(
                application_ids=[application.id for application in new_applications]
            )

        return UnifiedResponse(data=res)

