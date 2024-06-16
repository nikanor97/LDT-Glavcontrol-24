from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel

if TYPE_CHECKING:
    from src.db.projects.models.forecast import Forecast


class CompanyBase(ProjectsDataSQLModel):
    name: str = Field(nullable=False, index=True)
    region: str = Field(nullable=False)
    inn: str = Field(nullable=False)
    ogrn: str = Field(nullable=False)
    director: str = Field(nullable=False)
    foundation_date: date = Field(nullable=False)


class Company(CompanyBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "companies"
    forecast: list["Forecast"] = Relationship(back_populates="company")

