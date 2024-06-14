from io import BytesIO
from uuid import UUID

import pandas as pd
from starlette.responses import StreamingResponse

from src.db.projects.db_manager.remains import RemainsDbManager
from src.server.projects import ProjectsEndpoints


class ExportRemainsExcel(ProjectsEndpoints):
    async def call(
        self,
        remains_ids: list[UUID],
    ) -> StreamingResponse:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            remains = RemainsDbManager.get_remains_by_ids(
                session, remains_ids
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

