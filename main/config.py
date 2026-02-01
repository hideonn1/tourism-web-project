import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'bd_pjd'),
        charset="utf8mb4",
        collation="utf8mb4_general_ci"
    )