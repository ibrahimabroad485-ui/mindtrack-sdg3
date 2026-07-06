"""
Database access layer for MindTrack.

Handles SQLite connection management and schema initialization.
Kept separate from routes/analytics so storage concerns don't leak
into business logic.
"""
import sqlite3
import os
from datetime import date


def get_connection(db_path):
    """Return a SQLite connection with row access by column name."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    """Create the entries table if it doesn't already exist."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL UNIQUE,
            mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 10),
            sleep_hours REAL NOT NULL,
            exercised INTEGER NOT NULL CHECK (exercised IN (0, 1)),
            notes TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_entry(db_path, mood, sleep_hours, exercised, notes, entry_date=None):
    """Insert or update today's (or a given date's) wellness entry."""
    entry_date = entry_date or date.today().isoformat()
    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT INTO entries (entry_date, mood, sleep_hours, exercised, notes)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(entry_date) DO UPDATE SET
            mood=excluded.mood,
            sleep_hours=excluded.sleep_hours,
            exercised=excluded.exercised,
            notes=excluded.notes
        """,
        (entry_date, mood, sleep_hours, int(exercised), notes),
    )
    conn.commit()
    conn.close()


def fetch_all_entries(db_path):
    """Return all entries ordered by date ascending."""
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM entries ORDER BY entry_date ASC"
    ).fetchall()
    conn.close()
    return rows
