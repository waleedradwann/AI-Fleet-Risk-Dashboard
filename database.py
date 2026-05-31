import sqlite3

connection = sqlite3.connect("driver_monitoring.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT,
    confidence REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()

connection.close()

print("Database created successfully.")