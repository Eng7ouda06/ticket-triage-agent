import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # ensure the folder exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            message TEXT,
            urgency TEXT,
            category TEXT,
            summary TEXT,
            status TEXT,
            processed_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_ticket(ticket: dict, classification: dict, status: str):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (sender, subject, message, urgency, category, summary, status, processed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket["sender"],
        ticket["subject"],
        ticket["message"],
        classification["urgency"],
        classification["category"],
        classification["summary"],
        status,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_all_logged_tickets():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY processed_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows