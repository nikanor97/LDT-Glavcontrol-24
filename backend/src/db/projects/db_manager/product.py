from src.db.projects.db_manager import DbManager
from src.db.projects.models.product import Product


class ProductDbManager(DbManager):
    @staticmethod
    async def create_products(session, products) -> list[Product]:
        products = [Product(**product.dict()) for product in products]
        session.add_all(products)
        return products

