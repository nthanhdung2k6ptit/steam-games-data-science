
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

load_dotenv(BASE_DIR / ".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

csv_files = {
    "applications": "applications.csv",
    "categories": "categories.csv",
    "developers": "developers.csv",
    "genres": "genres.csv",
    "platforms": "platforms.csv",
    "publishers": "publishers.csv",
    "reviews": "reviews.csv",
    "application_categories": "application_categories.csv",
    "application_developers": "application_developers.csv",
    "application_genres": "application_genres.csv",
    "application_platforms": "application_platforms.csv",
    "application_publishers": "application_publishers.csv",
}

def import_csv_to_mysql():
    for table_name, file_name in csv_files.items():
        file_path = RAW_DATA_DIR / file_name
        if not file_path.exists():
            print(f"SKIP: {file_name} not found")
            continue
        print(f"Importing {file_name} -> table `{table_name}`")

        df = pd.read_csv(file_path, low_memory=False)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=5000
        )
        print(f"DONE: {table_name}, shape={df.shape}")
    print("All available CSV files imported successfully.")


if __name__ == "__main__":
    import_csv_to_mysql()