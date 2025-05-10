from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('flights.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/flights')
def get_flights():
    conn = get_db_connection()
    # Get flights from the last 5 minutes
    five_mins_ago = datetime.now(pytz.UTC) - timedelta(minutes=5)
    
    flights = conn.execute('''
        SELECT 
            icao24,
            callsign,
            altitude,
            speed,
            heading,
            lat,
            lon,
            squawk,
            timestamp
        FROM flights 
        WHERE timestamp > ?
        ORDER BY timestamp DESC
    ''', (five_mins_ago,)).fetchall()
    
    conn.close()
    
    return jsonify([dict(flight) for flight in flights])

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT icao24) as total_aircraft,
            MAX(altitude) as max_altitude,
            AVG(speed) as avg_speed
        FROM flights 
        WHERE timestamp > datetime('now', '-5 minutes')
    ''').fetchone()
    
    conn.close()
    return jsonify(dict(stats))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
