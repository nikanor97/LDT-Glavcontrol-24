# import pandas as pd
# from fastapi import UploadFile, File, HTTPException
#
# from src.db.projects.db_manager.procurement import ProcurementDbManager
# from src.db.projects.models.procurement import Procurement
# from src.server.common import UnifiedResponse
# from src.server.projects import ProjectsEndpoints
#
#
# COLUMN_MAPPING = {
#     "ID СПГЗ": "spgz_id",
#     "Наименование СПГЗ": "spgz_name",
#     "Дата заключения": "procurement_date",
#     "Цена ГК, руб.": "price",
#     "Способ определения поставщика": "way_to_define_supplier",
#     "Закон-основание (44/223)": "contract_basis"
# }
#
#
# class UploadProcurementsExcel(ProjectsEndpoints):
#     async def call(self, file: UploadFile = File(...)):
#         # Проверяем, что загруженный файл - это Excel
#         if not file.filename.endswith(('.xls', '.xlsx')):
#             raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")
#
#         # Читаем содержимое файла в DataFrame
#         try:
#             df = pd.read_excel(file.file)
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")
#
#         # Переименовываем столбцы в соответствии с маппингом
#         try:
#             df.rename(columns=COLUMN_MAPPING, inplace=True)
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=f"Error in column renaming: {e}")
#
#         # Проверяем, что все необходимые столбцы присутствуют
#         for col in COLUMN_MAPPING.values():
#             if col not in df.columns:
#                 raise HTTPException(status_code=400, detail=f"Missing required column: {col}")
#
#         # Преобразуем DataFrame в список словарей
#         records = df.to_dict(orient='records')
#
#         # Валидация данных с помощью Pydantic
#         procurements: list[Procurement] = []
#         for record in records:
#             try:
#                 procurement = Procurement(**record)
#                 procurements.append(procurement)
#             except Exception as e:
#                 raise HTTPException(status_code=400, detail=f"Error in data validation: {e}")
#
#         async with self._main_db_manager.projects.make_autobegin_session() as session:
#             # Сохраняем данные в базу
#             new_procurements = await ProcurementDbManager.create_procurements(session, procurements)
#
#         return UnifiedResponse(data=new_procurements)
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Annotated

import pandas as pd
from fastapi import UploadFile, File, HTTPException, Depends
from io import BytesIO

from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.procurement import Procurement
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
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
    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        file: UploadFile = File(...)
    ) -> UnifiedResponse[list[Procurement]]:
        user_id = get_user_id_from_token(token)

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)
        company_id = user_company.company_id

        # Проверяем, что загруженный файл - это Excel
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")

        # Читаем содержимое файла в DataFrame
        try:
            # Read the file content into a BytesIO object
            contents = await file.read()
            file_data = BytesIO(contents)
            df = pd.read_excel(file_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")

        # Переименовываем столбцы в соответствии с маппингом
        try:
            df.rename(columns=COLUMN_MAPPING, inplace=True)
            df = df.where(pd.notnull(df), None)
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
                price = record.get('price')
                if price is not None:
                    try:
                        # price = Decimal(price).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                        price = Decimal(int(price))
                        # print(price)
                    except Exception:
                        price = None  # or handle it as per your requirements

                procurement_date = record.get('procurement_date')
                if procurement_date is not None:
                    try:
                        procurement_date = datetime.strptime(procurement_date, '%d.%m.%Y')
                    except ValueError:
                        procurement_date = None  # or handle it as per your requirements

                try:
                    procurement = Procurement(
                        spgz_id=record.get("spgz_id"),
                        spgz_name=record.get("spgz_name"),
                        # procurement_date=datetime.strptime(record.get('procurement_date'), '%d.%m.%Y') if record.get(
                        #     'procurement_date') is not None else None,
                        procurement_date=procurement_date,
                        # price=Decimal(record.get('price')) if record.get('price') is not None else None,
                        price=price,
                        way_to_define_supplier=record.get('way_to_define_supplier'),
                        contract_basis=record.get('contract_basis'),
                        company_id=company_id
                    )
                    procurements.append(procurement)
                except Exception:
                    pass
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error in data validation: {e}")

        # print(procurements)

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            # Сохраняем данные в базу
            new_procurements = await ProcurementDbManager.create_procurements(session, procurements)

        return UnifiedResponse(data=new_procurements)
