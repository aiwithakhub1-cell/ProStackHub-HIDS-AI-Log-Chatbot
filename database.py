import os
import sqlite3
from datetime import datetime


DATABASE_PATH = "results/hids.db"


def initialize_database():
    os.makedirs("results", exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source_ip TEXT,
            log_message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_alert(event_type, severity, source_ip, log_message):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts (
            timestamp,
            event_type,
            severity,
            source_ip,
            log_message
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        event_type,
        severity,
        source_ip,
        log_message
    ))

    connection.commit()
    connection.close()


def get_alerts(limit=100):
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_alert_summary():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT severity, COUNT(*)
        FROM alerts
        GROUP BY severity
    """)

    rows = cursor.fetchall()

    connection.close()

    summary = {
        "total": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "critical": 0
    }

    for severity, count in rows:
        severity_key = severity.lower()

        if severity_key in summary:
            summary[severity_key] = count

        summary["total"] += count

    return summary