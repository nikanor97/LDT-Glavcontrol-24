from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from src.db.users.db_manager.user import UserDbManager
from src.db.users.db_manager.user_token import UserTokenDbManager
from src.server.auth_utils import create_user_token
from src.server.common import exc_to_str
from src.server.users.endpoints import UsersEndpoints


class SwaggerLoginForAccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_expires_at: int  # n_seconds to expiry
    refresh_expires_at: int  # n_seconds to expiry


class SwaggerLoginForAccessToken(UsersEndpoints):

    async def call(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> SwaggerLoginForAccessTokenResponse:

        async with self._main_db_manager.users.make_autobegin_session() as session:
            try:
                user = await UserDbManager.authenticate_user(
                    session, form_data.username, form_data.password
                )
            except NoResultFound as e:
                # return UnifiedResponse(error=, status_code=404)
                raise HTTPException(status_code=404, detail=exc_to_str(e))

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            # return UnifiedResponse(
            #     error="Incorrect username or password", status_code=401
            # )

        user_token_base = create_user_token(user)
        async with self._main_db_manager.users.make_autobegin_session() as session:
            try:
                user_token = await UserTokenDbManager.create_user_token(
                    session, user_token_base
                )
            except NoResultFound as e:
                # return UnifiedResponse(error=exc_to_str(e), status_code=500)
                raise HTTPException(
                    status_code=500,
                    detail="User can not be found, though credentials are correct. It's an internal error.",
                )

        token = SwaggerLoginForAccessTokenResponse(
            access_token=user_token.access_token,
            refresh_token=user_token.refresh_token,
            token_type=user_token.token_type,
            access_expires_at=(user_token.access_expires_at - datetime.now()).seconds,
            refresh_expires_at=(user_token.refresh_expires_at - datetime.now()).seconds,
        )

        return token
