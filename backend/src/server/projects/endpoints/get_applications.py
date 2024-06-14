from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetApplications(ProjectsEndpoints):

    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Application]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            applications = await ApplicationDbManager.get_applications(session, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=applications.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=applications.count),
                )
            )
