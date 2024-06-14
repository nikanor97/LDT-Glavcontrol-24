from typing import Annotated

from fastapi import Depends

from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.models.company import Company
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class GetCompany(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UnifiedResponse[Company]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            company = await CompanyDbManager.get_company_by_user(session, user_id)
            return UnifiedResponse(data=company)
