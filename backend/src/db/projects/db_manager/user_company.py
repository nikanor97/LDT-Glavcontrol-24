from sqlalchemy.ext.asyncio import AsyncSession

from src.db.projects.db_manager import DbManager
from src.db.projects.models.user_company import UserCompany


class UserCompanyDbManager(DbManager):
    @staticmethod
    async def create_user_company(
        session: AsyncSession,
        user_company: UserCompany
    ) -> UserCompany:
        session.add(user_company)
        return user_company
