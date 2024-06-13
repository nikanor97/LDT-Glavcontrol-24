from datetime import date
from decimal import Decimal

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class ProcurementBase(ProjectsDataSQLModel):
    spgz_id: str = Field(nullable=False)
    spgz_name: str = Field(nullable=False)
    procurement_date: date = Field(nullable=False)
    price: Decimal = Field(nullable=False)
    way_to_define_supplier: str = Field(nullable=False)
    contract_basis: str = Field(nullable=False)


class Procurement(ProcurementBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "procurements"
