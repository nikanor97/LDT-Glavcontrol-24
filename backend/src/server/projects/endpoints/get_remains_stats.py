from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.models.remains import Remains
from src.server.auth_utils import oauth2_scheme
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints
from src.server.projects.utils.calculate_quarter_dates import calculate_quarter_dates


class GetRemainsStatsResponse(BaseModel):
    saldo_begin_debet: Decimal
    saldo_begin_credit: Decimal
    saldo_period_debet: Decimal
    saldo_period_credit: Decimal
    saldo_end_debet: Decimal
    saldo_end_credit: Decimal


class GetRemainsStats(ProjectsEndpoints):

    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        year: int,
        quarter: int,
    ) -> UnifiedResponse[GetRemainsStatsResponse]:
        start_date, end_date = calculate_quarter_dates(year, quarter)

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            remains: list[Remains] = await RemainsDbManager.get_remains_for_period(
                session, start_date, end_date
            )

        res = GetRemainsStatsResponse(
            saldo_begin_debet=sum([r.saldo_begin_debet for r in remains if r.saldo_begin_debet is not None]),
            saldo_begin_credit=sum([r.saldo_begin_credit for r in remains if r.saldo_begin_credit is not None]),
            saldo_period_debet=sum([r.saldo_period_debet for r in remains if r.saldo_period_debet is not None]),
            saldo_period_credit=sum([r.saldo_period_credit for r in remains if r.saldo_period_credit is not None]),
            saldo_end_debet=sum([r.saldo_end_debet for r in remains if r.saldo_end_debet is not None]),
            saldo_end_credit=sum([r.saldo_end_credit for r in remains if r.saldo_end_credit is not None]),
        )

        return UnifiedResponse(data=res)
