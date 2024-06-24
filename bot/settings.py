from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    root_dir: Path = Path(__file__).parent.resolve()

    bot_token: str = "7009813125:AAE6_fnBgmrlRG8TDTKRbdMi5BErJSuQGW0"

    forecast_items_per_page: int = 5

    total_csv_filepath: str = "./total.csv"
    # total_names_json_filepath: str = "./total_item.json"
    kontract_names_json_filepath: str = "./items_kontr.json"
    recom_year_json_filepath: str = "./recoms_year.json"
    recom_q1_json_filepath: str = "./recoms_q1.json"
    recom_q2_json_filepath: str = "./recoms_q2.json"
    recom_q3_json_filepath: str = "./recoms_q3.json"
    recom_q4_json_filepath: str = "./recoms_q4.json"

    db_name_projects: str = "ldt_bpla_dev_projects"
    db_name_users: str = "ldt_bpla_dev_users"
    db_host: str = "localhost"
    db_port: int = 5445
    db_user: str = "postgres"
    db_password: str = "WSWwHfSx29tnMZFp"

settings = Settings()
