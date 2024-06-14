import pandas as pd
from fastapi import UploadFile, File, HTTPException

from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.models.remains import Remains
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


COLUMN_MAPPING = {
    "ЦМО": "cmo",
    "КОЦ": "koc",
    "Количество": "number",
    "Показатели": "indicator",
    "Сальдо на начало периода, дебет": "saldo_begin_debet",
    "Сальдо за период, дебет": "saldo_period_debet",
    "Сальдо за период, кредит": "saldo_period_credit",
    "Сальдо на конец периода, дебет": "saldo_end_debet",
}


class UploadRemainsExcel(ProjectsEndpoints):
    async def call(
        self,
        file: UploadFile = File(...)
    ) -> UnifiedResponse[list[Remains]]:
        # Проверяем, что загруженный файл - это Excel
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")

        # Читаем содержимое файла в DataFrame
        try:
            df = pd.read_excel(file.file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")

        # Переименовываем столбцы в соответствии с маппингом
        try:
            df.rename(columns=COLUMN_MAPPING, inplace=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error in column renaming: {e}")

        # Проверяем, что все необходимые столбцы присутствуют
        for col in COLUMN_MAPPING.values():
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

        # Преобразуем DataFrame в список словарей
        records = df.to_dict(orient='records')

        # Валидация данных с помощью Pydantic
        items: list[Remains] = []
        for record in records:
            try:
                item = Remains(**record)
                items.append(item)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error in data validation: {e}")

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            # Сохраняем данные в базу
            new_remains = await RemainsDbManager.create_remains(session, items)

        return UnifiedResponse(data=new_remains)
