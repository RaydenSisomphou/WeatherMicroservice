import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherService:
    def __init__(self):
        # The API key is stored in the .env file for security
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

            # Return the list of daily forecasts (up to 5 days)
            # The OpenWeatherMap API returns data in 3-hour intervals
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


def test_weather_service():
    # Initialize the WeatherService class
    weather_service = WeatherService()

    # Step 1: Get city name from user input
    city_name = input("Enter the city name: ")

    # Step 2: Get city coordinates using the WeatherService
    lat, lon = weather_service.get_coordinates(city_name)

    if lat is None or lon is None:
        print("City not found. Please check the city name and try again.")
        return

    # Step 3: Ask if user wants current weather or 7-day forecast
    print("\n1. Current Weather")
    print("2. 7 Day Forecast")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # Get current weather
        current_weather = weather_service.get_current_weather(lat, lon)
        if current_weather:
            print(f"\nWeather in {city_name}:")
            print(f"Temperature: {current_weather['main']['temp']}°C")
            print(f"Weather Conditions: {current_weather['weather'][0]['description']}")
            print(f"Humidity: {current_weather['main']['humidity']}%")
            print(f"Wind Speed: {current_weather['wind']['speed']} m/s")
        else:
            print("Error retrieving current weather.")

    elif choice == '2':
        # Get 7-day forecast
        forecast = weather_service.get_7_day_forecast(lat, lon)

        if forecast:
            print(f"\n7-Day Forecast for {city_name}:")
            for day in forecast:
                time = day['dt']  # This will be a timestamp, can be converted to readable date
                temperature = day['temp']['day']
                weather_description = day['weather'][0]['description']
                print(f"Date: {time}, Temp: {temperature}°C, Weather: {weather_description}")
        else:
            print("Error retrieving 7-day forecast.")

    else:
        print("Invalid choice. Please enter 1 or 2.")


# Run the test
if __name__ == "__main__":
    test_weather_service()
