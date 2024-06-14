from datetime import date
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import col

from src.db.common import ObjectsWithCount, paginated, count_objects
from src.db.projects.db_manager import DbManager
from src.db.projects.models.procurement import Procurement
from src.server.projects.utils.calculate_quarter_dates import calculate_quarter_dates


class ContractsStats(BaseModel):
    amount_contracts: int
    contracts_date: date


class ProcurementsStats(BaseModel):
    amount_contracts: int | None
    latest_contract_date: date | None
    contracts_stats: list[ContractsStats]


class ProcurementDbManager(DbManager):
    @staticmethod
    async def get_procurements_stats(
        session: AsyncSession,
        year: int,
        quarter: int,
    ) -> ProcurementsStats:
        """
        По заданному году и кварталу возвращает статистику по заключенным контрактам
        Возвращает данные за нужный период, вычислив их по дате заключения контракта
        :param session:
        :param year:
        :param quarter:
        :return:
        """

        start_date, end_date = calculate_quarter_dates(year, quarter)
        stmt = select(Procurement).where(
            (Procurement.procurement_date >= start_date) & (Procurement.procurement_date <= end_date)
        )
        procurements = (await session.execute(stmt)).scalars().all()

        amount_contracts = sum([p.price for p in procurements]) if len(procurements) > 0 else None
        latest_contract_date = max([procurement.contract_date for procurement in procurements]) if len(procurements) > 0 else None
        contracts_stats = []
        for month in range(1, 13):
            contracts_stats.append(
                ContractsStats(
                    amount_contracts=len([procurement for procurement in procurements if procurement.contract_date.month == month]),
                    contracts_date=date(year=year, month=month, day=1)
                )
            )
        return ProcurementsStats(
            amount_contracts=amount_contracts,
            latest_contract_date=latest_contract_date,
            contracts_stats=contracts_stats
        )

    @staticmethod
    async def get_procurements(
        session: AsyncSession,
        offset: int,
        limit: int
    ) -> ObjectsWithCount[list[Procurement]]:
        stmt = select(Procurement)
        procurements = await paginated(session, stmt, offset, limit)
        count = await count_objects(session, stmt)
        return ObjectsWithCount(objects=procurements, count=count)

    @staticmethod
    async def get_procurements_by_ids(
        session: AsyncSession,
        procurement_ids: list[UUID]
    ) -> list[Procurement]:
        stmt = select(Procurement).where(col(Procurement.id).in_(procurement_ids))
        procurements = (await session.execute(stmt)).scalars().all()
        return procurements

    @staticmethod
    async def create_procurements(
        session: AsyncSession,
        procurements: list[Procurement]
    ) -> list[Procurement]:
        for procurement in procurements:
            session.add(procurement)
        return procurements
