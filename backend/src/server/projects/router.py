from typing import Optional

from starlette.responses import FileResponse, StreamingResponse

import settings
from fastapi import APIRouter, Depends

from common.rabbitmq.publisher import Publisher
from src.db.main_db_manager import MainDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.company import Company
from src.db.projects.models.forecast import Forecast
from src.db.projects.models.procurement import Procurement
from src.db.projects.models.remains import Remains
from src.server.auth import Auth
from src.server.common import METHOD, UnifiedResponse, UnifiedResponsePaginated
from src.server.projects import ProjectsEndpoints
from src.server.projects.endpoints.create_application import CreateApplication, CreateApplicationResponse
from src.server.projects.endpoints.create_applications_by_forecast import CreateApplicationsFromForecast, \
    CreateApplicationsFromForecastResponse
from src.server.projects.endpoints.create_company import CreateCompany
from src.server.projects.endpoints.export_forecast_excel import ExportForecastExcel
from src.server.projects.endpoints.export_procurements_excel import ExportProcurementsExcel
from src.server.projects.endpoints.export_remains_excel import ExportRemainsExcel
from src.server.projects.endpoints.get_application import GetApplication, GetApplicationResponse
from src.server.projects.endpoints.get_application_document import GetApplicationDocument
from src.server.projects.endpoints.get_applications import GetApplications, GetApplicationsResponse
from src.server.projects.endpoints.get_companies import GetCompanies
from src.server.projects.endpoints.get_company import GetCompany
from src.server.projects.endpoints.get_forecast import GetForecast, GetForcastResponse
from src.server.projects.endpoints.get_forecast_json_full import GetForecastJsonFull
from src.server.projects.endpoints.get_procurements import GetProcurements
from src.server.projects.endpoints.get_procurements_stats import GetProcurementsStats, GetProcurementsStatsResponse
from src.server.projects.endpoints.get_remains import GetRemains
from src.server.projects.endpoints.get_remains_stats import GetRemainsStatsResponse, GetRemainsStats
from src.server.projects.endpoints.get_users_companies import GetUsersCompanies, UserWithCompany
from src.server.projects.endpoints.update_application import UpdateApplicationWithProducts, \
    UpdateApplicationWithProductsResponse
from src.server.projects.endpoints.update_company import UpdateCompany
from src.server.projects.endpoints.upload_procurements_excel import UploadProcurementsExcel
from src.server.projects.endpoints.upload_remains_excel import UploadRemainsExcel
from src.server.projects.models import ProcurementsStats, RemainsStats


class ProjectsRouter:
    def __init__(self, main_db_manager: MainDbManager, publisher: Publisher):
        # self._projects_endpoints = ProjectsEndpoints(main_db_manager, publisher)
        params = {"main_db_manager": main_db_manager, "publisher": publisher}

        self.router = APIRouter(
            prefix=f"{settings.API_PREFIX}/projects",
            # prefix=f"{settings.API_PREFIX}/markup",
            tags=["projects"],
        )

        self.router.add_api_route(
            path="/company-info",
            endpoint=GetCompany(**params).call,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-stats",
            endpoint=GetProcurementsStats(**params).call,
            response_model=UnifiedResponse[GetProcurementsStatsResponse],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-stats",
            endpoint=GetRemainsStats(**params).call,
            response_model=UnifiedResponse[GetRemainsStatsResponse],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements",
            endpoint=GetProcurements(**params).call,
            response_model=UnifiedResponsePaginated[list[Procurement]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-export-excel",
            endpoint=ExportProcurementsExcel(**params).call,
            response_class=StreamingResponse,
            methods=[METHOD.GET],
            # dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-upload-excel",
            endpoint=UploadProcurementsExcel(**params).call,
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/applications",
            endpoint=GetApplications(**params).call,
            response_model=UnifiedResponsePaginated[list[GetApplicationsResponse]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/application",
            endpoint=CreateApplication(**params).call,
            response_model=UnifiedResponse[CreateApplicationResponse],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/application",
            endpoint=GetApplication(**params).call,
            response_model=UnifiedResponse[GetApplicationResponse],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains",
            endpoint=GetRemains(**params).call,
            response_model=UnifiedResponsePaginated[list[Remains]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-export-excel",
            endpoint=ExportRemainsExcel(**params).call,
            response_class=StreamingResponse,
            methods=[METHOD.GET],
            # dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/remains-upload-excel",
            endpoint=UploadRemainsExcel(**params).call,
            response_model=UnifiedResponse[list[Remains]],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/forecast",
            endpoint=GetForecast(**params).call,
            response_model=UnifiedResponsePaginated[list[GetForcastResponse]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/forecast-export-excel",
            endpoint=ExportForecastExcel(**params).call,
            response_class=FileResponse,
            methods=[METHOD.GET],
            # dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/companies",
            endpoint=GetCompanies(**params).call,
            response_model=UnifiedResponsePaginated[list[Company]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/company",
            endpoint=CreateCompany(**params).call,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/company",
            endpoint=UpdateCompany(**params).call,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.PUT],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/users-companies",
            endpoint=GetUsersCompanies(**params).call,
            response_model=UnifiedResponsePaginated[list[UserWithCompany]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/forecast-json-full",
            endpoint=GetForecastJsonFull(**params).call,
            methods=[METHOD.GET],
            # dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/application",
            endpoint=UpdateApplicationWithProducts(**params).call,
            response_model=UnifiedResponse[UpdateApplicationWithProductsResponse],
            methods=[METHOD.PUT],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/applications-from-forecast",
            endpoint=CreateApplicationsFromForecast(**params).call,
            response_model=UnifiedResponse[CreateApplicationsFromForecastResponse],
            methods=[METHOD.POST],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/application-documents",
            endpoint=GetApplicationDocument(**params).call,
            response_model=UnifiedResponse[CreateApplicationsFromForecastResponse],
            methods=[METHOD.GET],
        )


