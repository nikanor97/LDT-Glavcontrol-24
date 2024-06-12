import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.db.projects.models import Company
from src.server.common import ModelWithLabelAndValue


class ProcurementsStats(BaseModel):
    pass


class RemainsStats(BaseModel):
    pass


class ApplicationCreate(BaseModel):
    pass


class CompanyCreate(BaseModel):
    pass
