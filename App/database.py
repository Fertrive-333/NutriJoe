# App/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "clinica.db"

def get_connection(): #Si no existe clinica.db la crea
    return sqlite3.connect(DB_PATH)

def init_db():
    #Crea la tabla si no existe
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tlf TEXT,
                gender TEXT,
                birthday TEXT
            )
        """)

def add_patient(name, tlf=None, gender=None, birthday=None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO patients (name, tlf, gender, birthday) VALUES (?, ?, ?, ?)",
            (name, tlf, gender, birthday),
        )