from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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

    @staticmethod
    async def get_all_users_companies(
        session: AsyncSession,
    ) -> list[UserCompany]:
        stmt = select(UserCompany)
        user_company = (await session.execute(stmt)).scalars().all()
        return user_company
