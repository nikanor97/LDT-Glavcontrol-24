from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from starlette.responses import FileResponse

import settings
from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.product import Product
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination, UnifiedResponse
from src.server.projects import ProjectsEndpoints


class GetApplicationDocument(ProjectsEndpoints):

    async def call(
        self,
        id: UUID,
    ) -> FileResponse:
        async with self._main_db_manager.projects.make_autobegin_session() as session:
            application = await ApplicationDbManager.get_application(session, id)
            # res = GetApplicationResponse(**application.dict(), products=application.products)
        # return UnifiedResponse(data=res)
        document_path = settings.BASE_DIR / "data" / "mock.docx"
        return FileResponse(document_path)
