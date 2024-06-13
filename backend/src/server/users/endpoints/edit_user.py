from pydantic import BaseModel

from src.db.users.models.user import User
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class EditUserRequest(BaseModel):
    name: str
    email: str
    permission_read_stat: bool
    permission_create_order: bool
    is_deleted: bool


class EditUser(UsersEndpoints):

    async def call(
        self,
        data: EditUserRequest
    ) -> UnifiedResponse[User]:
        pass
