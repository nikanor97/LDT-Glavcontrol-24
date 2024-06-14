from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.models.procurement import Procurement
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetProcurements(ProjectsEndpoints):

    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Procurement]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            procurements = await ProcurementDbManager.get_procurements(session, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=procurements.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=procurements.count),
                )
            )
