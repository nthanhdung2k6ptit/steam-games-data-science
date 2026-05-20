
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine


base_dir = Path(__file__).resolve().parent.parent

load_dotenv(base_dir / ".env")


def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")

    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
        "?charset=utf8mb4"
    )

    return engine
