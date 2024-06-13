from decimal import Decimal
from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class RemainsBase(ProjectsDataSQLModel):
    cmo: str | None = Field(nullable=False)
    koc: int | None = Field(nullable=False)
    number: int | None = Field(nullable=False)
    indicator: int | None = Field(nullable=False)
    saldo_begin_debet: Decimal | None = Field(nullable=False)
    saldo_begin_credit: Decimal | None = Field(nullable=False)
    saldo_period_debet: Decimal | None = Field(nullable=False)
    saldo_period_credit: Decimal | None = Field(nullable=False)
    saldo_end_debet: Decimal | None = Field(nullable=False)
    saldo_end_credit: Decimal | None = Field(nullable=False)
    product_id: UUID | None = Field(nullable=False, foreign_key="products.id")


class Remains(RemainsBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "remains"