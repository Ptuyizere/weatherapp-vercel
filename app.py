import os
import requests
import dotenv
from flask import Flask, request, render_template
from datetime import datetime, timezone
from typing import Dict, Tuple

# Load the API Key from the .env file
dotenv.load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
os.environ["WEATHER_API_KEY"] = api_key  # Optional: Set as environment variable for other libraries if needed

app = Flask(__name__)

def fetch_weather_info(city: str, suffix: str) -> Dict:
    """
    Retrieves the current weather report for a specified city using the OpenWeatherMap API.

    Args:
        city (str): The city name (already stripped of '+' or '++' suffixes).
        suffix (str): A string denoting the level of detail ('', '+', or '++').

    Returns:
        Dict: A dictionary containing weather information. The fields vary based on the suffix level.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city.lower(),
        "appid": api_key,
        "units": "metric"  # Returns temperature in Celsius
    }

    # Send GET request to OpenWeather API
    response = requests.get(url=base_url, params=params)

    if response.status_code == 200:
        # Extract key values from the response
        data = response.json()
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        tz = data["timezone"]
        dt = datetime.fromtimestamp(data["dt"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        visibility = data["visibility"]
        wind_speed = data["wind"]["speed"]
        descr = data["weather"][0]["description"]

        # Return partial, moderate, or full data depending on the suffix
        if suffix == "+":
            return {
                "latitude": lat,
                "longitude": lon,
                "date": dt,
                "temperature": temp,
                "feels_like": feels_like,
                "description": descr
            }
        elif suffix == "++":
            return {
                "latitude": lat,
                "longitude": lon,
                "timezone": tz,
                "date": dt,
                "temperature": temp,
                "feels_like": feels_like,
                "pressure": pressure,
                "humidity": humidity,
                "visibility": visibility,
                "wind_speed": wind_speed,
                "description": descr
            }
        else:
            return {
                "temperature": temp,
                "feels_like": feels_like,
                "description": descr
            }
    else:
        # Handle bad city names or API failures
        return {
            "error_message": f"No weather info for {city.lower()}"
        }

def split_suffix(string: str) -> Tuple[str, str]:
    """
    Splits a city input string into the city name and a suffix ('', '+', or '++').

    Args:
        string (str): The full user input, e.g., 'london++', 'paris+', or 'tokyo'.

    Returns:
        Tuple[str, str]: A tuple with (cleaned_city_name, suffix)
    """
    if string.endswith("++"):
        return string[:-2], '++'
    elif string.endswith("+"):
        return string[:-1], '+'
    else:
        return string, ''


# Main endpoint
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = {}
    error = None

    if request.method == "POST":
        city = request.form["city"]
        city, suffix = split_suffix(city.strip().lower())
        weather_data = fetch_weather_info(city, suffix)
        if "error" in weather_data:
            error = weather_data.pop("error")
    return render_template("index.html", data=weather_data, error=error)

if __name__ == '__main__':
    app.run()