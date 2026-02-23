import csv
import sqlite3
from pathlib import Path


def write_csv(data, out_path):
    fieldnames = [
        "text", "author", "tags",
        "born_date", "born_location", "description"
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore"   # ← ADD THIS
        )
        writer.writeheader()
        writer.writerows(data)

def write_sqlite(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        born_date TEXT,
        born_location TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY,
        text TEXT,
        author_id INTEGER,
        tags TEXT,
        UNIQUE(text, author_id),
        FOREIGN KEY(author_id) REFERENCES authors(id)
    )
    """)

    for item in data:
        cursor.execute("""
        INSERT OR IGNORE INTO authors(name, born_date, born_location, description)
        VALUES (?, ?, ?, ?)
        """, (item["author"], item["born_date"], item["born_location"], item["description"]))

        cursor.execute("SELECT id FROM authors WHERE name = ?", (item["author"],))
        author_id = cursor.fetchone()[0]

        cursor.execute("""
        INSERT OR IGNORE INTO quotes(text, author_id, tags)
        VALUES (?, ?, ?)
        """, (item["text"], author_id, item["tags"]))

    conn.commit()
    conn.close()

