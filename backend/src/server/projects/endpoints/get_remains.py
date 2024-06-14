from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.models.remains import Remains
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetRemains(ProjectsEndpoints):

    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Remains]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            remains = await RemainsDbManager.get_remains(session, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=remains.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=remains.count),
                )
            )
