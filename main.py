#!/usr/bin/env python3
import typer
import json
from pathlib import Path
from weather import get_weather, display_weather

app = typer.Typer()

DEFAULT_API_KEY = "e20353f1dc4145aca2e54937252505"  # Your API key
CONFIG_PATH = Path.home() / ".termweather.json"

def save_config(api_key: str):
    """Save API key to config file"""
    CONFIG_PATH.write_text(json.dumps({"api_key": api_key}))

def load_config():
    """Load API key from config file"""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())["api_key"]
    return None

@app.command()
def check(
    location: str = typer.Argument(..., help="City name or postal code"),
    api_key: str = typer.Option(None, help="WeatherAPI key (saves after first use)")
):
    """Check current weather and forecast"""
    # Use provided key, saved key, or default key
    key_to_use = api_key or load_config() or DEFAULT_API_KEY
    
    if not api_key and not load_config():
        save_config(DEFAULT_API_KEY)  # Save the default key if none exists
    
    weather_data = get_weather(key_to_use, location)
    display_weather(weather_data)

@app.command()
def setkey(api_key: str):
    """Set your WeatherAPI key"""
    save_config(api_key)
    print("✅ API key saved successfully!")

if __name__ == "__main__":
    app()