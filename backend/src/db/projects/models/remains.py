from decimal import Decimal
from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class RemainsBase(ProjectsDataSQLModel):
    cmo: str | None = Field(nullable=True)
    koc: int | None = Field(nullable=True)
    number: int | None = Field(nullable=True)
    indicator: int | None = Field(nullable=True)
    saldo_begin_debet: Decimal | None = Field(nullable=True)
    saldo_begin_credit: Decimal | None = Field(nullable=True)
    saldo_period_debet: Decimal | None = Field(nullable=True)
    saldo_period_credit: Decimal | None = Field(nullable=True)
    saldo_end_debet: Decimal | None = Field(nullable=True)
    saldo_end_credit: Decimal | None = Field(nullable=True)
    product_id: UUID | None = Field(nullable=True, foreign_key="products.id")  # TODO выкинуть нафиг
    company_id: UUID | None = Field(nullable=True, foreign_key="companies.id")


class Remains(RemainsBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "remains"