# track_adsb.py - Collects flight data from ADS-B receiver
import sqlite3
import requests
import time

def fetch_adsb_data():
    # Replace this URL with your ADS-B data source (e.g., dump1090)
    url = "http://your-adsb-receiver-ip/data.json"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("aircraft", [])
    except Exception as e:
        print(f"Error fetching ADS-B data: {e}")
        return []

def store_flight_data(flights):
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            callsign TEXT,
            altitude INTEGER,
            speed INTEGER,
            lat REAL,
            lon REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    for flight in flights:
        cursor.execute("""
            INSERT INTO flights (callsign, altitude, speed, lat, lon)
            VALUES (?, ?, ?, ?, ?)
        """, (flight.get("callsign", "Unknown"),
              flight.get("alt_baro", 0),
              flight.get("gs", 0),
              flight.get("lat", 0),
              flight.get("lon", 0)))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    while True:
        flights = fetch_adsb_data()
        store_flight_data(flights)
        print(f"Stored {len(flights)} flights in the database.")
        time.sleep(30)  # Fetch new data every 30 seconds
