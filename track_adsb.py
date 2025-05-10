# track_adsb.py - Collects flight data from ADS-B receiver
import sqlite3
import requests
import time
import logging
from datetime import datetime
import pytz

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flight_tracker.log'),
        logging.StreamHandler()
    ]
)

def fetch_adsb_data():
    """Fetch ADS-B data from dump1090 running on the Raspberry Pi"""
    # dump1090 typically runs on port 8080
    url = "http://localhost:8080/data.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("aircraft", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching ADS-B data: {e}")
        return []
    except ValueError as e:
        logging.error(f"Error parsing JSON data: {e}")
        return []

def store_flight_data(flights):
    """Store flight data in SQLite database"""
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icao24 TEXT,
            callsign TEXT,
            altitude INTEGER,
            speed INTEGER,
            heading INTEGER,
            lat REAL,
            lon REAL,
            squawk TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Get current time in UTC
    current_time = datetime.now(pytz.UTC)
    
    for flight in flights:
        try:
            cursor.execute("""
                INSERT INTO flights (
                    icao24, callsign, altitude, speed, heading,
                    lat, lon, squawk, timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                flight.get("hex", "Unknown"),
                flight.get("flight", "Unknown"),
                flight.get("alt_baro", 0),
                flight.get("gs", 0),
                flight.get("track", 0),
                flight.get("lat", 0),
                flight.get("lon", 0),
                flight.get("squawk", "0000"),
                current_time
            ))
        except Exception as e:
            logging.error(f"Error storing flight data: {e}")
            continue
    
    conn.commit()
    conn.close()

def cleanup_old_data():
    """Remove flight data older than 24 hours"""
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM flights 
            WHERE timestamp < datetime('now', '-24 hours')
        """)
        conn.commit()
    except Exception as e:
        logging.error(f"Error cleaning up old data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    logging.info("Starting flight tracker...")
    while True:
        try:
            flights = fetch_adsb_data()
            if flights:
                store_flight_data(flights)
                logging.info(f"Stored {len(flights)} flights in the database")
            
            # Clean up old data every hour
            if datetime.now().minute == 0:
                cleanup_old_data()
                
            time.sleep(5)  # Fetch new data every 5 seconds
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(30)  # Wait longer if there's an error
