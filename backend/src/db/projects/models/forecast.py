from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel

if TYPE_CHECKING:
    from src.db.projects.models.company import Company
    from src.db.projects.models.product import Product


class ForecastBase(ProjectsDataSQLModel):
    product_id: UUID | None = Field(nullable=False, foreign_key="products.id")
    quarter: int | None = Field(nullable=False)
    year: int | None = Field(nullable=False)
    company_id: UUID = Field(nullable=False, foreign_key="companies.id")


class Forecast(ForecastBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "forecasts"
    product: "Product" = Relationship()
    company: "Company" = Relationship(back_populates="forecast")
