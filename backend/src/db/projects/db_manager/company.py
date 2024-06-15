from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.company import Company
from src.db.projects.models.user_company import UserCompany


class CompanyDbManager(DbManager):

    @staticmethod
    async def get_company_by_user(
        session: AsyncSession,
        user_id: UUID
    ) -> Company:
        stmt = select(Company).where(
            (Company.id == UserCompany.company_id) & (UserCompany.user_id == UserCompany.user_id)
        )
        company = (await session.execute(stmt)).scalar()
        return company

    @staticmethod
    async def get_all_companies(
        session: AsyncSession,
    ) -> list[Company]:
        stmt = select(Company)
        companies = (await session.execute(stmt)).scalars().all()
        return companies

    @staticmethod
    async def get_companies(
        session: AsyncSession,
        offset: int,
        limit: int
    ) -> ObjectsWithCount[list[Company]]:
        stmt = select(Company)
        companies = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=companies, count=count)

    @staticmethod
    async def create_company(
        session: AsyncSession,
        company: Company
    ) -> Company:
        session.add(company)
        return company

    @staticmethod
    async def update_company(
        session: AsyncSession,
        company: Company
    ) -> Company:
        session.add(company)
        return company