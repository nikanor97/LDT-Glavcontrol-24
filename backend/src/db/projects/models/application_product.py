from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class ApplicationProductBase(ProjectsDataSQLModel):
    application_id: UUID = Field(nullable=False, foreign_key="applications.id")
    product_id: UUID = Field(nullable=False, foreign_key="products.id")


class ApplicationProduct(ApplicationProductBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "application_products"
    # __table_args__ = (UniqueConstraint("application_id", "product_id"),)
