# src/infra/database.py

from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

# Project root = folder that contains src/, tests/, pos.db, pyproject.toml, etc.
BASE_DIR = Path(__file__).resolve().parents[2]

# Our SQLite DB file in project root
DB_PATH = BASE_DIR / "pos.db"


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection]:
    conn = _get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """
    Initialize database schema for the Habit Tracker.
    Creates tables if they do not exist.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()

        # main habits table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,          -- 'boolean' | 'numeric'
                goal REAL,                   -- optional target value
                created_at TEXT NOT NULL,    -- ISO date string
                parent_id TEXT,              -- nullable, references habits(id)
                FOREIGN KEY (parent_id) REFERENCES habits(id)
                    ON DELETE CASCADE
            );
            """
        )

        # logs table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS habit_logs (
                id TEXT PRIMARY KEY,
                habit_id TEXT NOT NULL,
                date TEXT NOT NULL,          -- ISO date string
                value REAL NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
                    ON DELETE CASCADE
            );
            """
        )

        conn.commit()
    finally:
        conn.close()
