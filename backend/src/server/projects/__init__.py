import os
from collections import Counter, defaultdict
from decimal import Decimal
from io import BytesIO
from os.path import isfile, join
from typing import Annotated
from uuid import UUID

import aiofiles
import pandas as pd
from loguru import logger

import settings
from fastapi import Header, HTTPException, UploadFile, Depends
from sqlalchemy.exc import NoResultFound

from common.rabbitmq.publisher import Publisher

# from common.rabbitmq.client import RabbitClient
from src.db.exceptions import ResourceAlreadyExists
from src.db.main_db_manager import MainDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.company import Company
from src.db.projects.models.forecast import Forecast
from src.db.projects.models.procurement import Procurement
from src.db.projects.models.remains import Remains
from src.db.users.models import user
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse, exc_to_str, UnifiedResponsePaginated
from starlette.requests import Request
from starlette.responses import Response, FileResponse
from starlette.templating import Jinja2Templates

from src.server.projects.models import ProcurementsStats, RemainsStats, ApplicationCreate, CompanyCreate

# TODO: remove templates after testing
templates = Jinja2Templates(directory="templates")


class ProjectsEndpoints:
    def __init__(self, main_db_manager: MainDbManager, publisher: Publisher) -> None:
        self._main_db_manager = main_db_manager
        self._publisher = publisher
        # self._rabbit_client = RabbitClient()
        # await self._rabbit_client.connect()

    async def call(self, *args, **kwargs):
        raise NotImplementedError

    async def create_application(
        self,
        data: ApplicationCreate,
    ) -> UnifiedResponse[Application]:
        pass

    async def get_forecast(
        self,
        offset: int = 0,
        limit: int = 10,
        quarter: int | None = None,
    ) -> UnifiedResponsePaginated[list[Forecast]]:
        pass

    async def export_forecast_excel(
        self,
        quarter: int | None = None
    ) -> FileResponse:
        pass

    async def get_remains(
        self,
    ) -> UnifiedResponsePaginated[list[Remains]]:
        pass

    async def export_remains_excel(
        self
    ) -> FileResponse:
        # TODO: какие именно остатки экспортировать? Может по списку id?
        pass

    async def upload_remains_excel(
        self
    ) -> UnifiedResponse[list[Remains]]:
        pass

    async def get_companies(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Company]]:
        pass

    async def create_company(
        self,
        data: CompanyCreate,
    ) -> UnifiedResponse[Company]:
        pass

    async def edit_company(
        self,
        data: Company,
    ) -> UnifiedResponse[Company]:
        pass

    async def delete_companies(
        self,
        companies_ids: list[UUID],
    ) -> UnifiedResponse[list[Company]]:
        pass
