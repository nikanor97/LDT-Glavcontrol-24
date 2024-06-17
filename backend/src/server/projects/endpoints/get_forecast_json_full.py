import os

from fastapi import HTTPException
from starlette.responses import FileResponse

import settings
from src.server.projects import ProjectsEndpoints


class GetForecastJsonFull(ProjectsEndpoints):
    def call(self) -> FileResponse:
        file_path = os.path.join(settings.BASE_DIR / "data", "рекомендации.json")

        # Ensure the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Ensure it is a file
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail="Invalid file")

        return FileResponse(file_path, media_type='application/json')