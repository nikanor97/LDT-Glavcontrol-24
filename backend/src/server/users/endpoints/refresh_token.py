from datetime import datetime

from pydantic import BaseModel

from src.db.users.db_manager.user import UserDbManager
from src.db.users.db_manager.user_token import UserTokenDbManager
from src.server.auth_utils import TokenKind, get_user_id_from_token, create_user_token
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_expires_at: int  # n_seconds to expiry
    refresh_expires_at: int  # n_seconds to expiry


class RefreshToken(UsersEndpoints):
    async def call(
        self,
        refresh_token: str
    ) -> UnifiedResponse[RefreshTokenResponse]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            is_valid = await UserTokenDbManager.is_token_valid(
                session, refresh_token, token_kind=TokenKind.refresh
            )
            if not is_valid:
                return UnifiedResponse(
                    error="Refresh token has expired", status_code=401
                )

            user_id = get_user_id_from_token(refresh_token)

            user = await UserDbManager.get_user(session, user_id=user_id)

            user_token_base = create_user_token(user)

            new_user_token = await UserTokenDbManager.create_user_token(
                session, user_token_base
            )

            await UserTokenDbManager.invalidate_previous_token(
                session, refresh_token
            )

        token = RefreshTokenResponse(
            access_token=new_user_token.access_token,
            refresh_token=new_user_token.refresh_token,
            token_type=new_user_token.token_type,
            access_expires_at=(
                new_user_token.access_expires_at - datetime.now()
            ).seconds,
            refresh_expires_at=(
                new_user_token.refresh_expires_at - datetime.now()
            ).seconds,
        )
        return UnifiedResponse(data=token)
