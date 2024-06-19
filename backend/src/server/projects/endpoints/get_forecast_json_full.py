import os
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
        # TODO: отправлять два разных json, если quarter не указан, то отправлять за год, если указан, то за квартал
        file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации (1).json")

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Ensure it is a file
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail="Invalid file")

        return FileResponse(file_path, media_type='application/json')