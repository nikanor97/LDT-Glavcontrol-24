from typing import Annotated

from fastapi import Depends

from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetApplications(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Application]]:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            applications = await ApplicationDbManager.get_applications_by_author_id(session, user_id, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=applications.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=applications.count),
                )
            )  # TODO: добавить колво продуктов в заявке
