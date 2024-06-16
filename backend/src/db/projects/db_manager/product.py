from sqlalchemy.future import select
from sqlmodel import col

from src.db.projects.db_manager import DbManager
from src.db.projects.models.product import Product


class ProductDbManager(DbManager):
    @staticmethod
    async def create_products(session, products) -> list[Product]:
        products = [Product(**product.dict()) for product in products]
        session.add_all(products)
        return products

    @staticmethod
    async def update_products(session, products) -> list[Product]:
        # products_ids = [product.id for product in products]
        # stmt = select(Product).where(col(Product.id).in_(products_ids))
        # db_products = (await session.execute(stmt)).scalars().all()
        # product_id_to_product = {product.id: product for product in db_products}

        updated_products: list[Product] = []
        for product in products:
            # stmt = select(Product).where(Product.id == product.id)
            # db_product: Product = (await session.execute(stmt)).scalar_one()
            updated_products.append(await session.merge(product))
        return updated_products
