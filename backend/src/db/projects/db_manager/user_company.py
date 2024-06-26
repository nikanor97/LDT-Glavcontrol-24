from uuid import UUID

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
        user_company = UserCompany(**user_company.dict())
        session.add(user_company)
        return user_company

    @staticmethod
    async def get_all_users_companies(
        session: AsyncSession,
    ) -> list[UserCompany]:
        stmt = select(UserCompany)
        user_company = (await session.execute(stmt)).scalars().all()
        return user_company

    @staticmethod
    async def get_user_company_by_user_id(  # TODO: сейчас возвращает только первую запись
        session: AsyncSession,
        user_id: UUID
    ) -> UserCompany:
        stmt = select(UserCompany).where(UserCompany.user_id == user_id)
        user_company = (await session.execute(stmt)).scalars().first()
        return user_company
