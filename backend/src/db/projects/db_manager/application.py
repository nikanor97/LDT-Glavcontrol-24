from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.application import Application


class ApplicationDbManager(DbManager):
    @staticmethod
    async def get_applications_by_author_id(
        session: AsyncSession,
        author_id: UUID,
        offset: int,
        limit: int
    ) -> ObjectsWithCount[list[Application]]:
        stmt = select(Application).where(Application.author_id == author_id)
        applications = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=applications, count=count)

    @staticmethod
    async def get_application(
        session: AsyncSession,
        application_id: UUID
    ) -> Application:
        stmt = select(Application).where(Application.id == application_id).options(selectinload(Application.products))
        application = (await session.execute(stmt)).scalar_one()
        return application

    @staticmethod
    async def create_application(
        session: AsyncSession,
        application: Application
    ) -> Application:
        application = Application(**application.dict())
        session.add(application)
        return application

    @staticmethod
    async def create_applications(
        session: AsyncSession,
        application: list[Application]
    ) -> list[Application]:
        applications = [Application(**a.dict()) for a in application]
        session.add_all(applications)
        return applications

    @staticmethod
    async def update_application(
        session: AsyncSession,
        application: Application
    ) -> Application:
        stmt = select(Application).where(Application.id == application.id)
        db_application: Application = (await session.execute(stmt)).scalar_one()

        # db_application.calculation_id = application.calculation_id
        # db_application.lot_id = application.lot_id
        # db_application.client_id = application.client_id
        # db_application.shipment_start_date = application.shipment_start_date
        # db_application.shipment_end_date = application.shipment_end_date
        # db_application.shipment_volume = application.shipment_volume
        # db_application.shipment_address = application.shipment_address
        # db_application.shipment_terms = application.shipment_terms
        # db_application.year = application.year
        # db_application.gar_id = application.gar_id
        # db_application.spgz_end_id = application.spgz_end_id
        # db_application.amount = application.amount
        # db_application.unit_of_measurement = application.unit_of_measurement
        # db_application.status = application.status

        # application.status = db_application.status
        application.author_id = db_application.author_id

        updated_application = await session.merge(application)
        return updated_application
