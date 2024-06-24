import json
import os
import tempfile
from datetime import datetime
from io import BytesIO
from typing import Annotated
from uuid import UUID

import numpy as np
import pandas as pd
from fastapi import Depends
from loguru import logger
from starlette.responses import FileResponse, StreamingResponse

import settings
from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.db_manager.procurement import ProcurementDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.server.auth_utils import oauth2_scheme, get_user_id_from_token
from src.server.projects import ProjectsEndpoints


class ExportApplicationJson(ProjectsEndpoints):
    @logger.catch
    async def call(
        self,
        application_id: UUID,
    ) -> FileResponse:
        # user_id = get_user_id_from_token(token)
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            application = await ApplicationDbManager.get_application(session, application_id)

        # res = {
        #     "id": 1, # идетнификатор расчета
        #     "lotEntityId": 1, # Идентификатор лота
        #     "CustomerId":  1, # Идентификатор заказчика
        #     "rows": [ # Строки спецификации
        #         {
        #             "DeliverySchedule": { # График поставки
        #                 "dates": {
        #                     "end_date": " ", # Дата окончания поставки
        #                     "start_date": " " # Дата начала поставки
        #                 },
        #                 "deliveryAmount": 1 , # Объем поставки
        #                 "deliveryConditions": "", # Условия поставки
        #                 "year": 1 # Год
        #             },
        #             "address": { # Адрес поставки
        #                 "gar_id": " ", # Идентификатор ГАР
        #                 "text": " " # Адрес в текстовой форме
        #             },
        #             "entityId": 1 , # Сквозной идентификатор СПГЗ
        #             "id": 1 , # Идентификатор (версии) СПГЗ
        #             "nmc": 1 , # Сумма спецификации
        #             "okei_code": " ", # Ед. измерения по ОКЕИ
        #             "purchaseAmount": 1 ,# Объем поставки
        #             "spgzCharacteristics": [ # Характеристики СПГЗ. Заполняются в зависимости от типа характеристики в соответствии со структурой справочника СПГЗ
        #                 {
        #                     "characteristicName": " ",
        #                     "characteristicSpgzEnums": [
        #                         {
        #                             "value": " "
        #                         }
        #                     ],
        #                     "conditionTypeId": 1 ,
        #                     "kpgzCharacteristicId": 1 ,
        #                     "okei_id": 1 ,
        #                     "selectType": 1 ,
        #                     "typeId": 1 ,
        #                     "value1": 1 ,
        #                     "value2": 1
        #                 },
        #             ]
        #         }
        #     ]
        # }

        res = {
            "id": str(application.id), # идетнификатор расчета
            "lotEntityId": application.lot_id, # Идентификатор лота
            "CustomerId":  application.client_id, # Идентификатор заказчика
            # "rows": [ # Строки спецификации
            #     {
            #         "DeliverySchedule": { # График поставки
            #             "dates": {
            #                 "end_date": datetime.strftime(application.shipment_end_date, "%Y-%m-%d"), # Дата окончания поставки
            #                 "start_date": datetime.strftime(application.shipment_start_date, "%Y-%m-%d"), # Дата начала поставки
            #             },
            #             "deliveryAmount": application.amount , # Объем поставки
            #             "deliveryConditions": application.shipment_terms, # Условия поставки
            #             "year": application.year # Год
            #         },
            #         "address": { # Адрес поставки
            #             "gar_id": application.gar_id, # Идентификатор ГАР
            #             "text": application.shipment_address # Адрес в текстовой форме
            #         },
            #         "entityId": 1 , # Сквозной идентификатор СПГЗ
            #         "id": 1 , # Идентификатор (версии) СПГЗ
            #         "nmc": 1 , # Сумма спецификации
            #         "okei_code": " ", # Ед. измерения по ОКЕИ
            #         "purchaseAmount": 1 ,# Объем поставки
            #         "spgzCharacteristics": [ # Характеристики СПГЗ. Заполняются в зависимости от типа характеристики в соответствии со структурой справочника СПГЗ
            #             {
            #                 "characteristicName": " ",
            #                 "characteristicSpgzEnums": [
            #                     {
            #                         "value": " "
            #                     }
            #                 ],
            #                 "conditionTypeId": 1 ,
            #                 "kpgzCharacteristicId": 1 ,
            #                 "okei_id": 1 ,
            #                 "selectType": 1 ,
            #                 "typeId": 1 ,
            #                 "value1": 1 ,
            #                 "value2": 1
            #             },
            #         ]
            #     }
            # ]
        }

        products_jsons = [json.loads(product.meta) for product in application.products if product.meta is not None]
        print(application.products)

        none_to_list = lambda x: x if x is not None else []

        rows = [ # Строки спецификации
                {
                    "DeliverySchedule": { # График поставки
                        "dates": {
                            "end_date": datetime.strftime(application.shipment_end_date, "%Y-%m-%d"), # Дата окончания поставки
                            "start_date": datetime.strftime(application.shipment_start_date, "%Y-%m-%d"), # Дата начала поставки
                        },
                        "deliveryAmount": float(application.amount) , # Объем поставки
                        "deliveryConditions": application.shipment_terms, # Условия поставки
                        "year": application.year # Год
                    },
                    "address": { # Адрес поставки
                        "gar_id": application.gar_id, # Идентификатор ГАР
                        "text": application.shipment_address # Адрес в текстовой форме
                    },
                    "entityId": product_json.get('entityId') , # Сквозной идентификатор СПГЗ
                    "id": product_json.get('id') , # Идентификатор (версии) СПГЗ
                    "nmc": "", #"WHAT?????" , # Сумма спецификации
                    "okei_code": product_json['okeis'][0]['code'], # Ед. измерения по ОКЕИ  # TODO: их несколько
                    "purchaseAmount": float(product_json.get('amount')) ,# Объем поставки
                    "spgzCharacteristics": [ # Характеристики СПГЗ. Заполняются в зависимости от типа характеристики в соответствии со структурой справочника СПГЗ
                        {
                            "characteristicName": characteristic.get('characteristicName'),
                            "characteristicSpgzEnums": [
                                {
                                    "value": characteristic_enum.get('value')
                                } for characteristic_enum in none_to_list(characteristic.get('characteristicSpgzEnums', []))
                            ],
                            "conditionTypeId": characteristic.get('conditionTypeId') ,
                            "kpgzCharacteristicId": characteristic.get('kpgzCharacteristicId') ,
                            "okei_id": "", #"WHAT?????" ,
                            "selectType": "", #"WHAT?????" ,
                            "typeId": characteristic.get('valueTypeId') ,
                            "value1": characteristic.get('value1') ,
                            "value2": characteristic.get('value2')
                        } for characteristic in none_to_list(product_json.get('spgzCharacteristics', []))
                    ]
                } for product_json in products_jsons
            ]

        res['rows'] = rows

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8') as tmp_file:
            json.dump(res, tmp_file, ensure_ascii=False, indent=4)
            tmp_file_path = tmp_file.name

            # Возвращаем объединенный файл пользователю
            return FileResponse(tmp_file_path, media_type="application/json", filename=f"заявка.json")

