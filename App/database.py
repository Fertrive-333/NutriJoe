# App/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "clinica.db"

conn = sqlite3.connect(DB_PATH)

filas = conn.execute("SELECT id, name FROM patients").fetchall()

print(filas)
conn.close()