import json
import os
import tempfile
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import FileResponse

import settings
from src.server.projects import ProjectsEndpoints


class GetForecastJsonFull(ProjectsEndpoints):
    def call(
        self,
        user_id: UUID,
        year: int,
        quarter: int | None = None,
    ) -> FileResponse:
        if quarter == 1:
            file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации_1_квартал.json")
        elif quarter == 2:
            file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации_2_квартал.json")
        elif quarter == 3:
            file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации_3_квартал.json")
        elif quarter == 4:
            file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации_4_квартал.json")
        else:
            # Загружаем данные из всех JSON-файлов
            data = []
            for filename in [
                "рекомендации_1_квартал.json",
                "рекомендации_2_квартал.json",
                "рекомендации_3_квартал.json",
                "рекомендации_4_квартал.json",
            ]:
                with open(os.path.join(settings.BASE_DIR / "data", filename), "r") as f:
                    data.append(json.load(f))

            # Объединяем данные в один список или словарь (в зависимости от структуры ваших JSON-файлов)
            merged_data = []
            for item in data:
                if isinstance(item, list):
                    merged_data.extend(item)
                elif isinstance(item, dict):
                    merged_data.append(item)

            # Сохраняем объединенные данные во временный файл
            with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8') as tmp_file:
                json.dump(merged_data, tmp_file, ensure_ascii=False, indent=4)
                tmp_file_path = tmp_file.name

            # Возвращаем объединенный файл пользователю
            return FileResponse(tmp_file_path, media_type="application/json", filename="рекомендации.json")

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Ensure it is a file
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail="Invalid file")

        return FileResponse(file_path, media_type='application/json')