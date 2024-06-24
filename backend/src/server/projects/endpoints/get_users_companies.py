from datetime import date
from uuid import UUID

from loguru import logger
from pydantic import BaseModel

from src.db.projects.db_manager.company import CompanyDbManager
from src.db.projects.db_manager.user_company import UserCompanyDbManager
from src.db.projects.models.user_company import UserCompany
from src.db.users.db_manager.user import UserDbManager
from src.server.common import UnifiedResponsePaginated, DataWithPagination, Pagination
from src.server.projects import ProjectsEndpoints


class UserWithCompany(BaseModel):
    user_id: UUID
    user_name: str | None
    user_email: str
    user_permission_read_stat: bool
    user_permission_create_order: bool
    user_is_deleted: bool
    user_role: str
    user_telegram_username: str | None

    company_id: UUID | None
    company_name: str | None
    company_region: str | None
    company_inn: str | None
    company_ogrn: str | None
    company_director: str | None
    company_foundation_date: date | None


class GetUsersCompanies(ProjectsEndpoints):

    @logger.catch()
    async def call(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> UnifiedResponsePaginated[list[UserWithCompany]]:
        async with self._main_db_manager.users.make_autobegin_session() as session:
            users = await UserDbManager.get_all_users(session)

        async with self._main_db_manager.projects.make_autobegin_session() as session:
            companies = await CompanyDbManager.get_all_companies(session)
            users_companies: list[UserCompany] = await UserCompanyDbManager.get_all_users_companies(session)

        company_id_by_user_id = {user_company.user_id: user_company.company_id for user_company in users_companies}
        company_by_company_id = {company.id: company for company in companies}
        company_by_user_id = {user_id: company_by_company_id[company_id] for user_id, company_id in company_id_by_user_id.items() if user_id in company_id_by_user_id}

        users_pag = users[offset:offset+limit]

        res = [UserWithCompany(
            user_id=user.id,
            user_name=user.name,
            user_email=user.email,
            user_permission_read_stat=user.permission_read_stat,
            user_permission_create_order=user.permission_create_order,
            user_is_deleted=user.is_deleted,
            user_role=user.role,
            user_telegram_username=user.telegram_username,

            company_id=company_by_user_id[user.id].id if user.id in company_by_user_id else None,
            company_name=company_by_user_id[user.id].name if user.id in company_by_user_id else None,
            company_region=company_by_user_id[user.id].region if user.id in company_by_user_id else None,
            company_inn=company_by_user_id[user.id].inn if user.id in company_by_user_id else None,
            company_ogrn=company_by_user_id[user.id].ogrn if user.id in company_by_user_id else None,
            company_director=company_by_user_id[user.id].director if user.id in company_by_user_id else None,
            company_foundation_date=company_by_user_id[user.id].foundation_date if user.id in company_by_user_id else None,
        ) for user in users_pag]

        return UnifiedResponsePaginated(
            data=DataWithPagination(
                items=res,
                pagination=Pagination(offset=offset, limit=limit, count=len(res)),
            )
        )
