"""
Seeds the database with sample entries for demo purposes.

Run from project root:
    python data/seed.py
"""
import sys
import os
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db import init_db, insert_entry

DB_PATH = "data/mindtrack.db"


def seed(days=21):
    init_db(DB_PATH)
    today = date.today()
    for i in range(days, 0, -1):
        entry_date = (today - timedelta(days=i)).isoformat()
        exercised = random.random() > 0.5
        mood = random.randint(6, 9) if exercised else random.randint(3, 7)
        sleep_hours = round(random.uniform(5.5, 8.5), 1)
        insert_entry(DB_PATH, mood, sleep_hours, exercised, "", entry_date=entry_date)
    print(f"Seeded {days} days of sample data into {DB_PATH}")


if __name__ == "__main__":
    seed()
