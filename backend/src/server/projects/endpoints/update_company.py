from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.models.company import Company
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class UpdateCompanyRequest(BaseModel):
    id: UUID
    name: str
    region: str
    inn: str
    ogrn: str
    director: str
    foundation_date: date


class UpdateCompany(ProjectsEndpoints):
    async def call(
        self,
        data: UpdateCompanyRequest,
    ) -> UnifiedResponse[Company]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            company = Company(**data.dict())
            new_company = await CompanyDbManager.update_company(
                session, company
            )
        return UnifiedResponse(data=new_company)

