from datetime import date
from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class CompanyBase(ProjectsDataSQLModel):
    name: str = Field(nullable=False, index=True)
    region: str = Field(nullable=False)
    inn: str = Field(nullable=False)
    ogrn: str = Field(nullable=False)
    owner_id: UUID = Field(nullable=False)
    foundation_date: date = Field(nullable=False)


class Company(CompanyBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "companies"
