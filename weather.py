import requests
from pathlib import Path
import json

def get_weather(api_key: str, location: str) -> dict:
    """Fetch weather data from WeatherAPI"""
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3&aqi=no&alerts=no"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def display_weather(data: dict):
    """Display formatted weather data"""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return

    location = data["location"]
    current = data["current"]
    forecast = data["forecast"]["forecastday"]

    # Weather icons mapping
    icons = {
        "sunny": "☀️ ",
        "clear": "☀️ ",
        "rain": "🌧️ ",
        "cloudy": "☁️ ",
        "partly cloudy": "⛅ ",
        "snow": "❄️ ",
        "thunder": "⛈️ ",
        "mist": "🌫️ "
    }

    # Get appropriate icon
    condition = current["condition"]["text"].lower()
    icon = icons.get(condition, "🌡️ ")

    print(f"\n{icon} Weather for {location['name']}, {location['country']}:")
    print(f"📍 {location['localtime']}")
    print(f"  Temperature: {current['temp_c']}°C (Feels like {current['feelslike_c']}°C)")
    print(f"  Condition: {current['condition']['text']}")
    print(f"  Wind: {current['wind_kph']} km/h, Humidity: {current['humidity']}%")
    print(f"  UV Index: {current['uv']}")

    print("\n📅 3-Day Forecast:")
    for day in forecast:
        date = day["date"]
        high = day["day"]["maxtemp_c"]
        low = day["day"]["mintemp_c"]
        condition = day["day"]["condition"]["text"]
        icon = icons.get(condition.lower(), "🌡️ ")
        print(f"  {icon} {date}: {high}°C / {low}°C, {condition}")