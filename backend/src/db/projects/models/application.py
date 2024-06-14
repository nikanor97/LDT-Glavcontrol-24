from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class ApplicationBase(ProjectsDataSQLModel):
    calculation_id: str | None = Field(nullable=True)
    lot_id: str | None = Field(nullable=True)
    client_id: str | None = Field(nullable=True)
    shipment_start_date: date | None = Field(nullable=True)
    shipment_end_date: date | None = Field(nullable=True)
    shipment_volume: int | None = Field(nullable=True)
    shipment_address: str | None = Field(nullable=True)
    shipment_terms: str | None = Field(nullable=True)
    year: int | None = Field(nullable=True)
    gar_id: str | None = Field(nullable=True)
    spgz_end_id: str | None = Field(nullable=True)
    amount: Decimal | None = Field(nullable=True)
    unit_of_measurement: str | None = Field(nullable=True)

    author_id: UUID | None = Field(nullable=True)
    status: str | None = Field(nullable=False)  # draft | ready  # TODO: add enum


class Application(ApplicationBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "applications"
