# WeatherApp (Web + Docker Support)

WeatherApp is a simple Python application that fetches and displays current weather information using the [OpenWeatherMap API](https://openweathermap.org/api). You can run it locally or in a Docker container.

---

## Features

- Search weather by city name
- `+` suffix: returns more details (temperature, feels like, coordinates, etc.)
- `++` suffix: returns extended details (pressure, humidity, wind, etc.)
- Web interface using Flask
- Docker support for containerized deployment
- Clean tabular CLI output and styled HTML for web output

---

## Prerequisites

- Python 3.8+
- [OpenWeatherMap API Key](https://home.openweathermap.org/users/sign_up)
- Docker (optional, for container deployment)

---

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weatherapp.git
   cd weatherapp

2. **Create .env file**
WEATHER_API_KEY=your_api_key_here

3. Install dependencies
pip install -r requirements.txt

## Usage

1. Start the Flask app
python app.py

2. Visit
http://localhost:8000

3. Enter city name with optional + or ++ for extended info.

## Run with Docker

1. Build the image
docker build -t weatherapp

2. Run the container
docker run -d -p 8080:8000 --env-file .env weatherapp

vist http://localhost:8080

## Example Output

+--------------+----------------------+
| Property     | Value                |
+--------------+----------------------+
| temperature  | 22.3°C               |
| feels_like   | 21.8°C               |
| description  | light rain           |
+--------------+----------------------+
