from uuid import UUID

from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel
from src.db.projects.models.product import Product


class ForecastBase(ProjectsDataSQLModel):
    product_id: UUID | None = Field(nullable=False, foreign_key="products.id")
    quarter: int | None = Field(nullable=False)
    year: int | None = Field(nullable=False)


class Forecast(ForecastBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "forecasts"
    product: Product = Relationship()
