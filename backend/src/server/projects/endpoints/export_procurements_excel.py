from io import BytesIO
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import Depends
from starlette.responses import FileResponse, StreamingResponse

from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.projects import ProjectsEndpoints


class ExportProcurementsExcel(ProjectsEndpoints):
    async def call(
        self,
        # token: Annotated[str, Depends(oauth2_scheme)],
        user_id: UUID,
    ) -> StreamingResponse:
        # user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)
            procurements = await ProcurementDbManager.get_all_procurements(
                session, user_company.company_id
            )

        df = pd.DataFrame([p.dict() for p in procurements])

        # Создаем BytesIO объект
        buffer = BytesIO()

        # Записываем DataFrame в BytesIO как Excel
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Перематываем buffer к началу
        buffer.seek(0)

        # Возвращаем файл как ответ
        return StreamingResponse(
            buffer,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment;filename=data.xlsx'}
        )

