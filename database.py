# database.py
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    # Мы используем yield вместо return.
    # FastAPI сам закроет соединение, когда функция отработает.
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            yield cur
            conn.commit()