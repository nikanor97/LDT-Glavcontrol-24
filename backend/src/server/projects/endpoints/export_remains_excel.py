from io import BytesIO
from typing import Annotated
from uuid import UUID

import numpy as np
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
        user_id: UUID,
        # token: Annotated[str, Depends(oauth2_scheme)],
    ) -> StreamingResponse:
        # user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)
            remains = await RemainsDbManager.get_all_remains(
                session, user_company.company_id
            )

        # df = pd.DataFrame([p.dict() for p in remains])
        df = pd.DataFrame({
            "ЦМО": [r.cmo for r in remains],
            "КОЦ": [r.koc for r in remains],
            "Количество": [r.number for r in remains],
            "Показатели": [r.indicator for r in remains],
            "Сальдо на начало периода. Дебет": [r.saldo_begin_debet for r in remains],
            "Сальдо за период. Дебет": [r.saldo_period_debet for r in remains],
            "Сальдо за период. Кредит": [r.saldo_period_credit for r in remains],
            "Сальдо на конец периода. Дебет": [r.saldo_end_debet for r in remains],
        })
        df = df.replace({np.nan: None})
        df = df.dropna()
        df['Сальдо на начало периода. Дебет'] = df['Сальдо на начало периода. Дебет'].astype(int)
        df['Сальдо за период. Дебет'] = df['Сальдо за период. Дебет'].astype(int)
        df['Сальдо за период. Кредит'] = df['Сальдо за период. Кредит'].astype(int)
        df['Сальдо на конец периода. Дебет'] = df['Сальдо на конец периода. Дебет'].astype(int)

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

