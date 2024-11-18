import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherService:
    def __init__(self):
        # The API key is stored in the .env file for security but can just be entered here
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.geo_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_coordinates(self, city_name):
        # Get coordinates of the city
        params = {
            'q': city_name,
            'appid': self.api_key
        }
        try:
            response = requests.get(self.geo_url, params=params)
            response.raise_for_status()  # Will raise an exception for bad status
            data = response.json()
            lat = data['coord']['lat']
            lon = data['coord']['lon']
            return lat, lon
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving coordinates: {e}")
            return None, None

    def get_current_weather(self, lat, lon):
        # Fetch current weather data for a given city
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.geo_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving current weather: {e}")
            return None

    def get_5_day_forecast(self, lat, lon):
        # Fetch 5-day forecast
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Return the list of daily forecasts, the OpenWeatherMap API returns data in 3-hour intervals
            forecast = []
            for i in range(0, len(data['list']), 8):  # Every 8th entry is a 24-hour period (3 hours * 8 = 24)
                day = data['list'][i]
                forecast.append({
                    "dt": day['dt'],
                    "temp": day['main']['temp'],
                    "weather": day['weather'][0]['description']
                })

            return forecast[:5]  # Only return 5 days of forecast
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving 5-day forecast: {e}")
            return None
# v2.0