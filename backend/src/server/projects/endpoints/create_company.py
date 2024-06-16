from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.models.company import Company
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class CreateCompanyRequest(BaseModel):
    name: str
    region: str
    inn: str
    ogrn: str
    director: str
    foundation_date: date


class CreateCompany(ProjectsEndpoints):
    async def call(
        self,
        data: CreateCompanyRequest,
    ) -> UnifiedResponse[Company]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            company = Company(**data.dict())
            new_company = await CompanyDbManager.create_company(
                session, company
            )
        return UnifiedResponse(data=new_company)

