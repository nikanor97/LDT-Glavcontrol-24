import os
import uuid
from collections import Counter, defaultdict
from decimal import Decimal
from io import BytesIO
from os.path import isfile, join
from typing import Optional, Annotated

import aiofiles
import ffmpeg  # type: ignore
import pandas as pd
from loguru import logger

import settings
from fastapi import Header, HTTPException, UploadFile, Depends
from sqlalchemy.exc import NoResultFound

from common.rabbitmq.publisher import Publisher

# from common.rabbitmq.client import RabbitClient
from src.db.exceptions import ResourceAlreadyExists
from src.db.main_db_manager import MainDbManager
from src.db.users.models import User
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse, exc_to_str
from starlette.requests import Request
from starlette.responses import Response, FileResponse
from starlette.templating import Jinja2Templates


# TODO: remove templates after testing
templates = Jinja2Templates(directory="templates")


class ProjectsEndpoints:
    def __init__(self, main_db_manager: MainDbManager, publisher: Publisher) -> None:
        self._main_db_manager = main_db_manager
        self._publisher = publisher
        # self._rabbit_client = RabbitClient()
        # await self._rabbit_client.connect()
