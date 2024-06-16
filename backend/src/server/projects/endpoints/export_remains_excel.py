from io import BytesIO
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import Depends
from starlette.responses import StreamingResponse

from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.projects import ProjectsEndpoints


class ExportRemainsExcel(ProjectsEndpoints):
    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        remains_ids: list[UUID],
    ) -> StreamingResponse:
        user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)
            remains = await RemainsDbManager.get_all_remains(
                session, user_company.company_id
            )

        df = pd.DataFrame([p.dict() for p in remains])

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

