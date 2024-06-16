from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel
from src.db.projects.models.application_product import ApplicationProduct

if TYPE_CHECKING:
    from src.db.projects.models.application import Application


class ProductBase(ProjectsDataSQLModel):
    name: str | None = Field(nullable=False)
    price: Decimal | None = Field(nullable=False)
    number: int | None = Field(nullable=False)
    amount: Decimal | None = Field(nullable=False)


class Product(ProductBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "products"
    application: "Application" = Relationship(
        back_populates="products",
        link_model=ApplicationProduct,
    )