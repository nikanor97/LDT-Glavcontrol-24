from datetime import date
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.server.auth_utils import oauth2_scheme
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


class ContractsStats(BaseModel):
    amount_contracts: int
    contracts_date: date


class GetProcurementsStatsResponse(BaseModel):
    amount_contracts: int | None
    latest_contract_date: date | None
    contracts_stats: list[ContractsStats]


class GetProcurementsStats(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        year: int | None,
        quarter: int | None,
    ) -> UnifiedResponse[GetProcurementsStatsResponse]:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            procurements_stats = await ProcurementDbManager.get_procurements_stats(
                session, year, quarter
            )
            return UnifiedResponse(data=procurements_stats)
