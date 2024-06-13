from uuid import UUID

from src.db.users.models.user import User
from src.server.common import UnifiedResponse
from src.server.users.endpoints import UsersEndpoints


class GetUser(UsersEndpoints):

    async def call(
        self,
        user_id: UUID
    ) -> UnifiedResponse[User]:
        pass
