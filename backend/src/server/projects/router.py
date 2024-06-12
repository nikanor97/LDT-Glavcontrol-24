from typing import Optional

import settings
from fastapi import APIRouter, Depends

from common.rabbitmq.publisher import Publisher
from src.db.main_db_manager import MainDbManager
from src.server.auth import Auth
from src.server.common import METHOD, UnifiedResponse
from src.server.projects.endpoints import ProjectsEndpoints


class ProjectsRouter:
    def __init__(self, main_db_manager: MainDbManager, publisher: Publisher):
        self._projects_endpoints = ProjectsEndpoints(main_db_manager, publisher)

        self.router = APIRouter(
            prefix=f"{settings.API_PREFIX}/projects",
            # prefix=f"{settings.API_PREFIX}/markup",
            tags=["projects"],
        )

        self.router.add_api_route(
            path="/company",
            endpoint=self._projects_endpoints.get_company,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/procurements-stats",
            endpoint=self._projects_endpoints.get_company,
            response_model=UnifiedResponse[Company],
            methods=[METHOD.GET],
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


