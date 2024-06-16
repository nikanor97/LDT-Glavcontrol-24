from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.projects.db_manager import DbManager
from src.db.projects.models.application_product import ApplicationProduct


class ApplicationProductDbManager(DbManager):
    @staticmethod
    async def create_application_products(
        session: AsyncSession,
        application_products: list[ApplicationProduct]
    ) -> list[ApplicationProduct]:
        application_products = [ApplicationProduct(**application_product.dict()) for application_product in application_products]
        session.add_all(application_products)
        return application_products

    @staticmethod
    async def update_application_products(
        session: AsyncSession,
        application_id: UUID,
        products_ids: list[UUID]
    ) -> list[ApplicationProduct]:
        # Тут надо удалить старые связи (product_id которых отсутствует в products_ids) и создать новые
        stmt = select(ApplicationProduct).where(ApplicationProduct.application_id == application_id)
        old_application_products: list[ApplicationProduct] = (await session.execute(stmt)).scalars().all()
        for application_product in old_application_products:
            if application_product.product_id not in products_ids:
                await session.delete(application_product)

        existing_products_ids = {application_product.product_id for application_product in old_application_products}
        new_application_products = [ApplicationProduct(
            application_id=application_id,
            product_id=product_id
        ) for product_id in products_ids if product_id not in existing_products_ids]
        session.add_all(new_application_products)

        await session.flush()

        stmt = select(ApplicationProduct).where(ApplicationProduct.application_id == application_id)
        application_products: list[ApplicationProduct] = (await session.execute(stmt)).scalars().all()
        return application_products
