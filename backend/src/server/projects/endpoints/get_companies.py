from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.models.company import Company
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetCompanies(ProjectsEndpoints):

    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Company]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            applications = await CompanyDbManager.get_companies(session, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=applications.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=applications.count),
                )
            )
