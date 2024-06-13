from typing import Annotated

from fastapi import Depends
from jose import JWTError
from sqlalchemy.exc import NoResultFound

from src.db.users.db_manager.user import UserDbManager
from src.db.users.models.user import User
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.common import UnifiedResponse, exc_to_str
from src.server.users.endpoints import UsersEndpoints


class GetCurrentUser(UsersEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UnifiedResponse[User]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            try:
                user_id = get_user_id_from_token(token)
                user = await UserDbManager.get_user(
                    session, user_id=user_id
                )
            except NoResultFound as e:
                return UnifiedResponse(error=exc_to_str(e), status_code=404)
            except JWTError as e:
                return UnifiedResponse(error=exc_to_str(e), status_code=401)
        return UnifiedResponse(data=user)