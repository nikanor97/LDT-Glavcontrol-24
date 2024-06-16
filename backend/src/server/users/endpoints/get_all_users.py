from src.db.users.db_manager.user import UserDbManager
from src.db.users.models.user import User
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class GetAllUsers(UsersEndpoints):

    async def call(self) -> UnifiedResponse[list[User]]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            users = await UserDbManager.get_all_users(session)
        return UnifiedResponse(data=users)
