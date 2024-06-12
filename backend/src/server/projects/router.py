from typing import Optional

from starlette.responses import FileResponse

import settings
from fastapi import APIRouter, Depends

from common.rabbitmq.publisher import Publisher
from src.db.main_db_manager import MainDbManager
from src.db.projects.models import Company, Procurement, Forecast, Application, Remains
from src.server.auth import Auth
from src.server.common import METHOD, UnifiedResponse, UnifiedResponsePaginated
from src.server.projects.endpoints import ProjectsEndpoints
from src.server.projects.models import ProcurementsStats, RemainsStats


class ProjectsRouter:
    def __init__(self, main_db_manager: MainDbManager, publisher: Publisher):
        self._projects_endpoints = ProjectsEndpoints(main_db_manager, publisher)

        self.router = APIRouter(
            prefix=f"{settings.API_PREFIX}/projects",
            # prefix=f"{settings.API_PREFIX}/markup",
            tags=["projects"],
        )

        self.router.add_api_route(
            path="/company-info",
            endpoint=self._projects_endpoints.get_company,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-stats",
            endpoint=self._projects_endpoints.get_procurements_stats,
            response_model=UnifiedResponse[ProcurementsStats],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-stats",
            endpoint=self._projects_endpoints.get_remains_stats,
            response_model=UnifiedResponse[RemainsStats],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements",
            endpoint=self._projects_endpoints.get_procurements,
            response_model=UnifiedResponsePaginated[list[Procurement]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-export-excel",
            endpoint=self._projects_endpoints.export_procurements_excel,
            response_class=FileResponse,
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-upload-excel",
            endpoint=self._projects_endpoints.upload_procurements_excel,
            response_model=UnifiedResponse[list[Procurement]],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/application",
            endpoint=self._projects_endpoints.create_application,
            response_model=UnifiedResponse[Application],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/forecast",
            endpoint=self._projects_endpoints.get_forecast,
            response_model=UnifiedResponsePaginated[list[Forecast]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/forecast-export-excel",
            endpoint=self._projects_endpoints.export_forecast_excel,
            response_class=FileResponse,
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains",
            endpoint=self._projects_endpoints.get_remains,
            response_model=UnifiedResponsePaginated[list[Remains]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-export-excel",
            endpoint=self._projects_endpoints.export_remains_excel,
            response_class=FileResponse,
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-upload-excel",
            endpoint=self._projects_endpoints.upload_remains_excel,
            response_model=UnifiedResponse[list[Remains]],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

# ------------------------------------------------------------------------------------------------

        self.router.add_api_route(
            path="/companies",
            endpoint=self._projects_endpoints.get_companies,
            response_model=UnifiedResponsePaginated[list[Company]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/company",
            endpoint=self._projects_endpoints.create_company,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/company",
            endpoint=self._projects_endpoints.edit_company,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.PUT],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/companies",
            endpoint=self._projects_endpoints.delete_companies,
            response_model=UnifiedResponsePaginated[list[Company]],
            methods=[METHOD.DELETE],
            dependencies=[Depends(Auth(main_db_manager))],
        )















        # self.router.add_api_route(
        #     path="/create-upload-video",
        #     endpoint=self._projects_endpoints.create_and_upload_video,
        #     response_model=UnifiedResponse[Video],
        #     methods=[METHOD.POST],
        #     dependencies=[Depends(Auth(main_db_manager))],
        #     tags=["projects"],
        # )
        #
        # self.router.add_api_route(
        #     path="/frames-with-markups",
        #     endpoint=self._projects_endpoints.create_frames_with_markups,
        #     response_model=UnifiedResponse[list[FrameMarkup]],
        #     methods=[METHOD.POST],
        #     dependencies=[Depends(Auth(main_db_manager))],
        #     tags=["bpla"]
        # )


