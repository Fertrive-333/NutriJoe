# App/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "clinica.db"


def get_connection():
    """Devuelve una conexión a la base de datos (la crea si no existe)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias si no existen."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tlf TEXT,
                gender TEXT,
                birthday TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories REAL,
                protein REAL,
                carbs REAL,
                fat REAL
            )
        """)


def add_patient(name, tlf=None, gender=None, birthday=None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO patients (name, tlf, gender, birthday) VALUES (?, ?, ?, ?)",
            (name, tlf, gender, birthday),
        )


def add_food(name, calories=0.0, protein=0.0, carbs=0.0, fat=0.0):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO foods (name, calories, protein, carbs, fat) VALUES (?, ?, ?, ?, ?)",
            (name, calories, protein, carbs, fat),
        )


def get_all_foods():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, calories, protein, carbs, fat FROM foods ORDER BY name COLLATE NOCASE"
        ).fetchall()
        return [dict(row) for row in rows]