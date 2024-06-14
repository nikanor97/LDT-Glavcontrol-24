from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from src.db.exceptions import ResourceAlreadyExists
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


class CreateUser(UsersEndpoints):
    async def call(
        self,
        user_create: CreateUserRequest
    ) -> UnifiedResponse[User]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            try:
                user = UserBase(**user_create.dict())
                new_user = await UserDbManager.create_user(session, user)

                await UserPasswordDbManager.create_user_password(
                    session, new_user.id, user_create.password
                )

                return UnifiedResponse(data=new_user)
            except ResourceAlreadyExists as e:
                return UnifiedResponse(error=exc_to_str(e), status_code=409)
            except NoResultFound as e:
                return UnifiedResponse(error=exc_to_str(e), status_code=404)
