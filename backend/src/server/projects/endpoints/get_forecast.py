from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.models.forecast import Forecast
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class GetForecast(ProjectsEndpoints):

    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[Forecast]]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            forecast = await ForecastDbManager.get_forecast(session, offset, limit)
            return UnifiedResponsePaginated(
                data=DataWithPagination(
                    items=forecast.objects,
                    pagination=Pagination(offset=offset, limit=limit, count=forecast.count),
                )
            )
