from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).parent.resolve()
    bot_token: str = "7009813125:AAE6_fnBgmrlRG8TDTKRbdMi5BErJSuQGW0"


settings = Settings()
