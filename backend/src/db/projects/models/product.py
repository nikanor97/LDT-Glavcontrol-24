from decimal import Decimal

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class ProductBase(ProjectsDataSQLModel):
    name: str | None = Field(nullable=False)
    price: Decimal | None = Field(nullable=False)
    number: int | None = Field(nullable=False)
    amount: Decimal | None = Field(nullable=False)


class Product(ProductBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "products"
