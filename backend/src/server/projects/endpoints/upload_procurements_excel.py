import pandas as pd
from fastapi import UploadFile, File, HTTPException

from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.models.procurement import Procurement
from src.server.common import UnifiedResponse
from src.server.projects import ProjectsEndpoints


COLUMN_MAPPING = {
    "ID СПГЗ": "spgz_id",
    "Наименование СПГЗ": "spgz_name",
    "Дата заключения": "procurement_date",
    "Цена ГК, руб.": "price",
    "Способ определения поставщика": "way_to_define_supplier",
    "Закон-основание (44/223)": "contract_basis"
}


class UploadProcurementsExcel(ProjectsEndpoints):
    async def call(self, file: UploadFile = File(...)):
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
        procurements: list[Procurement] = []
        for record in records:
            try:
                procurement = Procurement(**record)
                procurements.append(procurement)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error in data validation: {e}")

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            # Сохраняем данные в базу
            new_procurements = await ProcurementDbManager.create_procurements(session, procurements)

        return UnifiedResponse(data=new_procurements)
