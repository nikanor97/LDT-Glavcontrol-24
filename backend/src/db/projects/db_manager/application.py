from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.application import Application


class ApplicationDbManager(DbManager):
    @staticmethod
    async def get_applications(
        session: AsyncSession,
        offset: int,
        limit: int
    ) -> ObjectsWithCount[list[Application]]:
        stmt = select(Application)
        applications = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=applications, count=count)

    @staticmethod
    async def create_application(
        session: AsyncSession,
        application: Application
    ) -> Application:
        return await Application.create(session, application)
