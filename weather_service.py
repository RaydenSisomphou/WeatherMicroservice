import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()  # Load api key from .env file

app = Flask(__name__)  # Initialize Flask app


class WeatherService:
    def __init__(self):
        # Initialize API key and URLs for weather data
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.geocode_url = "http://api.openweathermap.org/geo/1.0/direct"

    def get_coordinates(self, city_name):
        # Get latitude and longitude for a given city
        params = {
            'q': city_name,
            'limit': 1,
            'appid': self.api_key
        }
        response = requests.get(self.geocode_url, params=params)
        response.raise_for_status()  # Check for errors
        data = response.json()
        return data[0]['lat'], data[0]['lon']  # Return coordinates

    def get_5_day_forecast(self, lat, lon):
        # Get 5-day weather forecast based on coordinates
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # Return temperature in Celsius
        }
        response = requests.get(self.forecast_url, params=params)
        response.raise_for_status()  # Check for errors
        data = response.json()
        forecast = []
        for i in range(0, len(data['list']), 8):  # Get forecast every 8 hours (for 5 days)
            day = data['list'][i]
            forecast.append({
                "dt": day['dt'],  # Date and time
                "temp": day['main']['temp'],  # Temperature
                "weather": day['weather'][0]['description'],  # Weather description
                "weather_id": day['weather'][0]['id'],  # Weather condition ID
                "wind": day['wind'],  # Wind data
                "main": day['main']  # Main weather data (temp, pressure, humidity)
            })
        return forecast[:5]  # Return only the first 5 days


weather_service = WeatherService()  # Initialize weather service


# API Routes
@app.route('/get-coordinates', methods=['GET'])
def get_coordinates():
    # Route to get city coordinates
    city_name = request.args.get('city')
    lat, lon = weather_service.get_coordinates(city_name)
    return jsonify({'latitude': lat, 'longitude': lon})  # Return coordinates


@app.route('/5-day-forecast', methods=['GET'])
def five_day_forecast():
    # Route to get 5-day weather forecast
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    forecast = weather_service.get_5_day_forecast(lat, lon)
    return jsonify(forecast)  # Return forecast


if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app in debug mode

    #