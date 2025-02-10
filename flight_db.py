import sqlite3

# Connect to SQLite database (creates flights.db if it doesn't exist)
conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

# Create table to store flight data
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    callsign TEXT,
    altitude REAL,
    speed REAL,
    latitude REAL,
    longitude REAL,
    timestamp TEXT
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database 'flights.db' created successfully.")
