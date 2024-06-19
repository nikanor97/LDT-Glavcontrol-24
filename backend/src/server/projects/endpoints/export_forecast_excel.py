from io import BytesIO
from typing import Annotated
from uuid import UUID

import numpy as np
import pandas as pd
from fastapi import Depends
from starlette.responses import StreamingResponse, FileResponse

from src.db.projects.db_manager.forecast import ForecastDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.projects import ProjectsEndpoints


class ExportForecastExcel(ProjectsEndpoints):
    async def call(
        self,  # TODO: добавить год и квартал и если ids пустые то исходя из года и квартала сформировать
        user_id: UUID,
        year: int,
        quarter: int | None = None,
    ) -> FileResponse:
        # user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)

            if quarter is None:
                quarter = 1
            forecast = await ForecastDbManager.get_all_forecast(
                session, user_company.company_id, quarter, year,
            )

        # df = pd.DataFrame([p.dict() for p in forecast])
        df = pd.DataFrame({
            "Наименование": [f.product.name for f in forecast],
            "Цена": [f.product.price for f in forecast],
            "Количество": [f.product.number for f in forecast],
            "Сумма": [f.product.amount for f in forecast],
        })
        df = df.replace({np.nan: None})
        df = df.dropna()
        df['Цена'] = df['Цена'].astype(int)
        df['Сумма'] = df['Сумма'].astype(int)

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

