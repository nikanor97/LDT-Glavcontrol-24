from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from src.db.exceptions import ResourceAlreadyExists
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.user_company import UserCompany
from src.db.users.db_manager.user import UserDbManager
from src.db.users.db_manager.user_password import UserPasswordDbManager
from src.db.users.models.user import User, UserBase
from src.server.common import UnifiedResponse, exc_to_str
from src.server.users.endpoints import UsersEndpoints


class CreateUserRequest(BaseModel):
    name: str
    email: str
    permission_read_stat: bool
    permission_create_order: bool
    is_deleted: bool
    password: str
    role: str = "user"
    company_id: UUID
    telegram_username: str | None


class CreateUser(UsersEndpoints):
    async def call(
        self,
        user_create: CreateUserRequest
    ) -> UnifiedResponse[User]:
        async with self._main_db_manager.projects.make_autobegin_session() as projects_session:
            async with self._main_db_manager.users.make_autobegin_session() as session:
                try:
                    user = UserBase(**user_create.dict())
                    new_user = await UserDbManager.create_user(session, user)

                    await UserPasswordDbManager.create_user_password(
                        session, new_user.id, user_create.password
                    )

                    user_company = UserCompany(
                        user_id=new_user.id, company_id=user_create.company_id
                    )
                    await UserCompanyDbManager.create_user_company(
                        projects_session, user_company
                    )

                    return UnifiedResponse(data=new_user)
                except ResourceAlreadyExists as e:
                    return UnifiedResponse(error=exc_to_str(e), status_code=409)
                except NoResultFound as e:
                    return UnifiedResponse(error=exc_to_str(e), status_code=404)
