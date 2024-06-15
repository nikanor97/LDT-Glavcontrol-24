from uuid import UUID

from sqlmodel import Field

from src.db.mixins import TimeStampWithIdMixin
from src.db.projects.models import ProjectsDataSQLModel


class UserCompanyBase(ProjectsDataSQLModel):
    user_id: UUID | None = Field(nullable=False)
    company_id: UUID | None = Field(nullable=False, foreign_key="companies.id")


class UserCompany(UserCompanyBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "user_companies"
