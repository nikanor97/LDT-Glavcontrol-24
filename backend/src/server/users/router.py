import settings
from fastapi import APIRouter, Depends
from src.db.main_db_manager import MainDbManager
from src.db.users.models.user import User
from src.server.auth import Auth
from src.server.common import METHOD, UnifiedResponse
from src.server.users.endpoints import UsersEndpoints
from src.server.users.endpoints.create_user import CreateUser
from src.server.users.endpoints.delete_user import DeleteUser
from src.server.users.endpoints.update_user import UpdateUser
from src.server.users.endpoints.get_all_users import GetAllUsers
from src.server.users.endpoints.get_current_user import GetCurrentUser
from src.server.users.endpoints.get_user import GetUser
from src.server.users.endpoints.login_for_access_token import LoginForAccessToken, LoginForAccessTokenResponse
from src.server.users.endpoints.refresh_token import RefreshToken, RefreshTokenResponse
from src.server.users.endpoints.swagger_login_for_access_token import SwaggerLoginForAccessToken, \
    SwaggerLoginForAccessTokenResponse


class UsersRouter:
    def __init__(
        self,
        main_db_manager: MainDbManager,
    ):
        # self._endpoints = UsersEndpoints(main_db_manager)
        params = {"main_db_manager": main_db_manager}

        self.router = APIRouter(
            prefix=f"{settings.API_PREFIX}/users",
            tags=["users"],
        )

        self.router.add_api_route(
            path="/user",
            endpoint=CreateUser(**params).call,
            response_model=UnifiedResponse[User],
            methods=[METHOD.POST],
        )

        self.router.add_api_route(
            path="/token",
            endpoint=LoginForAccessToken(**params).call,
            response_model=UnifiedResponse[LoginForAccessTokenResponse],
            methods=[METHOD.POST],
        )

        self.router.add_api_route(
            path="/swagger-token",
            endpoint=SwaggerLoginForAccessToken(**params).call,
            response_model=SwaggerLoginForAccessTokenResponse,
            methods=[METHOD.POST],
        )

        self.router.add_api_route(
            path="/token-refresh",
            endpoint=RefreshToken(**params).call,
            response_model=UnifiedResponse[RefreshTokenResponse],
            methods=[METHOD.POST],
        )

        self.router.add_api_route(
            path="/me",
            endpoint=GetCurrentUser(**params).call,
            response_model=UnifiedResponse[User],
            methods=[METHOD.GET],
        )

        self.router.add_api_route(
            path="/users-all",
            endpoint=GetAllUsers(**params).call,
            response_model=UnifiedResponse[list[User]],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/user",
            endpoint=UpdateUser(**params).call,
            response_model=UnifiedResponse[User],
            methods=[METHOD.PUT],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/user",
            endpoint=DeleteUser(**params).call,
            response_model=UnifiedResponse[User],
            methods=[METHOD.DELETE],
            dependencies=[Depends(Auth(main_db_manager))],
        )

        self.router.add_api_route(
            path="/user",
            endpoint=GetUser(**params).call,
            response_model=UnifiedResponse[User],
            methods=[METHOD.GET],
            dependencies=[Depends(Auth(main_db_manager))],
        )
