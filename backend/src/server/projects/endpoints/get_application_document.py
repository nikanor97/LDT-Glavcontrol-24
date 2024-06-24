import tempfile
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from starlette.responses import FileResponse

import settings
from src.db.projects.db_manager.application import ApplicationDbManager
from src.db.projects.models.application import Application
from src.db.projects.models.product import Product
from src.server import properties
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination, UnifiedResponse
from src.server.generate_docs import generate_docx
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
        # document_path = settings.BASE_DIR / "data" / "mock.docx"

        # Создание временного файла для выходного документа
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx_file:
            output_file_path = temp_docx_file.name

            products_dict = [p.dict() for p in application.products]

            # Генерация DOCX документа
            generate_docx(products_dict, properties.item_properties, output_file_path)
            print(f"Документ '{output_file_path}' был успешно создан.")

            # Возвращаем созданный документ пользователю
            return FileResponse(
                output_file_path,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                filename=f"ТЗ_заявка_{datetime.strftime(application.created_at, '%y%m%d-%H%M%S')}.docx"
            )
