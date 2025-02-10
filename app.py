from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

OPENSKY_URL = "https://opensky-network.org/api/states/all"

def fetch_flights():
    response = requests.get(OPENSKY_URL)
    if response.status_code == 200:
        data = response.json()
        flights = []
        for flight in data.get('states', []):
            if flight[5] and flight[6]:  # Check if lat/lon are available
                flights.append([
                    flight[1],  # Callsign
                    flight[7],  # Altitude
                    flight[9],  # Speed
                    flight[6],  # Latitude
                    flight[5],  # Longitude
                    flight[4]   # Timestamp
                ])
        return flights
    return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flights')
def flights():
    return jsonify(fetch_flights())

if __name__ == '__main__':
    app.run(debug=True)
