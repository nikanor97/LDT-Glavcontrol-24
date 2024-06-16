from src.db.main_db_manager import MainDbManager


class UsersEndpoints:
    def __init__(
        self,
        main_db_manager: MainDbManager,
    ) -> None:
        self._main_db_manager = main_db_manager

    async def call(self, *args, **kwargs):
        raise NotImplementedError
