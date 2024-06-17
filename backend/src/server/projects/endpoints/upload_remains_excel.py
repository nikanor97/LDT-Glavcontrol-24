from decimal import Decimal
from io import BytesIO
from typing import Annotated

import numpy as np
import pandas as pd
from fastapi import UploadFile, File, HTTPException, Depends
from loguru import logger

from src.db.projects.db_manager.product import ProductDbManager
from src.db.projects.db_manager.remains import RemainsDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.product import Product
from src.db.projects.models.remains import Remains
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
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
    @logger.catch()
    async def call(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        file: UploadFile = File(...),
    ) -> UnifiedResponse[list[Remains]]:
        user_id = get_user_id_from_token(token)
        # Проверяем, что загруженный файл - это Excel
        if not file.filename.endswith(('.xls', '.xlsx')):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")

        # Читаем содержимое файла в DataFrame
        try:
            # Read the file content into a BytesIO object
            contents = await file.read()
            file_data = BytesIO(contents)
            df = pd.read_excel(file_data)
            df = df[5:-1]
            df = df.replace({np.nan: None})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading Excel file: {e}")

        # Переименовываем столбцы в соответствии с маппингом
        try:
            df.rename(columns=COLUMN_MAPPING, inplace=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error in column renaming: {e}")

        # # Проверяем, что все необходимые столбцы присутствуют
        # for col in COLUMN_MAPPING.values():
        #     if col not in df.columns:
        #         raise HTTPException(status_code=400, detail=f"Missing required column: {col}")

        # Преобразуем DataFrame в список словарей
        # records = df.to_dict(orient='records')

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            user_company = await UserCompanyDbManager.get_user_company_by_user_id(session, user_id)

        # Валидация данных с помощью Pydantic
        items: list[Remains] = []
        products: list[Product] = []
        for row in df.iterrows():
            row = row[1]
            try:
                # cmo: str | None = Field(nullable=True)
                # koc: int | None = Field(nullable=True)
                # number: int | None = Field(nullable=True)
                # indicator: int | None = Field(nullable=True)
                # saldo_begin_debet: Decimal | None = Field(nullable=True)
                # saldo_begin_credit: Decimal | None = Field(nullable=True)
                # saldo_period_debet: Decimal | None = Field(nullable=True)
                # saldo_period_credit: Decimal | None = Field(nullable=True)
                # saldo_end_debet: Decimal | None = Field(nullable=True)
                # saldo_end_credit: Decimal | None = Field(nullable=True)
                # product_id: UUID | None = Field(nullable=True, foreign_key="products.id")  # TODO выкинуть нафиг
                # company_id: UUID | None = Field(nullable=True, foreign_key="companies.id")
                # name = row[df.columns[3]]
                # if name is None:
                #     name = "Unknown"
                # number = row[df.columns[5]]
                # if number is None:
                #     number = 0

                product = Product(
                    name=row[df.columns[3]] or "Unknown",
                    price=Decimal(1),
                    number=row[df.columns[5]] or 0,
                    amount=Decimal(1),
                )
                products.append(product)

                item = Remains(
                    cmo=row[df.columns[3]],
                    koc=row[df.columns[2]],
                    number=row[df.columns[5]],
                    indicator=None,
                    saldo_begin_debet=row[df.columns[6]],
                    # saldo_begin_credit=record[df.columns[7]],
                    saldo_period_debet=row[df.columns[8]],
                    saldo_period_credit=row[df.columns[10]],
                    saldo_end_debet=row[df.columns[12]],
                    # saldo_end_credit=record[12],
                    company_id=user_company.company_id,
                    product_id=product.id
                )

                items.append(item)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error in data validation: {e}")

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            new_products = await ProductDbManager.create_products(session, products)
            await session.flush()
            new_remains = await RemainsDbManager.create_remains(session, items)

        return UnifiedResponse(data=new_remains)
