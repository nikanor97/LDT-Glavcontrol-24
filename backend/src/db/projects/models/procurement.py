from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class ProcurementBase(ProjectsDataSQLModel):
    spgz_id: str | None = Field(nullable=True)
    spgz_name: str | None = Field(nullable=True)
    procurement_date: date | None = Field(nullable=True)
    price: Decimal | None = Field(nullable=True)
    way_to_define_supplier: str | None = Field(nullable=True)
    contract_basis: str | None = Field(nullable=True)
    company_id: UUID = Field(nullable=False, foreign_key="companies.id")


class Procurement(ProcurementBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "procurements"
