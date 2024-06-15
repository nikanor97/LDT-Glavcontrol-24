from src.db.projects.db_manager import DbManager


class ProductDbManager(DbManager):
    @staticmethod
    async def create_products(session, products):
        session.add_all(products)

