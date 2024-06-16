from typing import Annotated

from fastapi import Depends

from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.remains import Remains
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetRemains(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Remains]]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)

            remains = await RemainsDbManager.get_remains(session, user_company.company_id, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=remains.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=remains.count),
                )
            )
