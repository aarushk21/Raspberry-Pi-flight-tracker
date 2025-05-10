# Raspberry Pi Flight Tracker

A real-time flight tracking system built with Raspberry Pi that displays aircraft information in a modern web interface. This project uses ADS-B signals to track aircraft in your vicinity and presents the data in an organized, user-friendly format.

## Features

- Real-time flight tracking using ADS-B signals
- Modern, responsive web interface
- Live statistics including:
  - Total aircraft in range
  - Maximum altitude
  - Average speed
- Detailed flight information:
  - Callsign
  - ICAO24 (unique aircraft identifier)
  - Altitude
  - Speed
  - Heading
  - Squawk code
  - Last update time
- Automatic data cleanup (24-hour retention)
- Error logging and monitoring

## Hardware Requirements

- Raspberry Pi (3B+ or newer recommended)
- RTL-SDR USB dongle (for receiving ADS-B signals)
- Antenna suitable for 1090 MHz (ADS-B frequency)

## Software Requirements

- Python 3.7+
- dump1090 (ADS-B decoder)
- Required Python packages (see requirements.txt)

## Installation

1. Install dump1090:
```bash
sudo apt-get update
sudo apt-get install dump1090-fa
```

2. Clone this repository:
```bash
git clone https://github.com/aarushk21/Raspberry-Pi-flight-tracker.git
cd Raspberry-Pi-flight-tracker
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start dump1090:
```bash
sudo systemctl start dump1090-fa
```

2. Start the flight tracker:
```bash
python track_adsb.py
```

3. In a separate terminal, start the web interface:
```bash
python app.py
```

4. Access the flight tracker by opening a web browser and navigating to:
```
http://your-raspberry-pi-ip:5000
```

## Project Structure

- `track_adsb.py`: Main script for collecting and storing flight data
- `app.py`: Flask web server for the user interface
- `index.html`: Web interface template
- `style.css`: Custom styling for the web interface
- `requirements.txt`: Python package dependencies
- `flights.db`: SQLite database for storing flight data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- dump1090 for ADS-B decoding
- Flask for the web framework
- Bootstrap for the UI components 