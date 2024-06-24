from uuid import UUID

from pydantic import BaseModel

from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.user_company import UserCompany
from src.db.users.models.user import User
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class UpdateUserRequest(BaseModel):
    user_id: UUID
    company_id: UUID
    name: str
    email: str
    permission_read_stat: bool
    permission_create_order: bool
    is_deleted: bool
    telegram_username: str | None


class UpdateUser(UsersEndpoints):

    async def call(
        self,
        data: UpdateUserRequest
    ) -> UnifiedResponse[User]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            user = await User.by_id(session, data.user_id)
            user.name = data.name
            user.email = data.email
            user.permission_read_stat = data.permission_read_stat
            user.permission_create_order = data.permission_create_order
            user.is_deleted = data.is_deleted
            user.telegram_username = data.telegram_username

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            uc = UserCompany(
                user_id=data.user_id,
                company_id=data.company_id
            )
            await UserCompanyDbManager.create_user_company(
                session, uc
            )

        return UnifiedResponse(data=user)