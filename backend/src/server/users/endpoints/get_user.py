from uuid import UUID

from src.db.users.db_manager.user import UserDbManager
from src.db.users.models.user import User
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class GetUser(UsersEndpoints):

    async def call(
        self,
        user_id: UUID
    ) -> UnifiedResponse[User]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            user = await UserDbManager.get_user(session, user_id=user_id)
        return UnifiedResponse(data=user)
