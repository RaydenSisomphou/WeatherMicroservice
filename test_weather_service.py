import requests
from datetime import datetime, timezone


def test_weather_service():
    # Get city name from user input
    city_name = input("Enter the city name: ")

    # Call the API to get coordinates for the city
    geo_url = "http://127.0.0.1:5000/get-coordinates"
    response = requests.get(geo_url, params={'city': city_name})

    # Check if city was found
    if response.status_code != 200:
        print("City not found. Please check the city name and try again.")
        return

    # Extract latitude and longitude from the response
    data = response.json()
    lat = data['latitude']
    lon = data['longitude']

    # Call the API to get 5-day forecast using coordinates
    forecast_url = "http://127.0.0.1:5000/5-day-forecast"
    forecast_response = requests.get(forecast_url, params={'lat': lat, 'lon': lon})

    # Process the forecast if the response is successful
    if forecast_response.status_code == 200:
        forecast = forecast_response.json()
        print(f"\n5-Day Forecast for {city_name}:")

        # Define weather symbols for different weather conditions
        sun_symbol = "☀️"
        cloud_symbol = "☁️"
        snowflake_symbol = "❄️"
        rain_symbol = "☔️"


        # Loop through each day's forecast data
        for day in forecast:
            time = day['dt']
            temperature = day['temp']
            weather_description = day['weather']
            wind_speed = day.get('wind', {}).get('speed', 'N/A')
            humidity = day.get('main', {}).get('humidity', 'N/A')
            weather_id = day['weather_id']

            # Convert timestamp to readable date format
            date = datetime.fromtimestamp(time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

            # Determine the weather icon based on weather condition ID
            if weather_id >= 200 and weather_id < 300:
                weather_icon = rain_symbol
            elif weather_id >= 300 and weather_id < 400:
                weather_icon = cloud_symbol
            elif weather_id >= 500 and weather_id < 600:
                weather_icon = rain_symbol
            elif weather_id >= 600 and weather_id <= 622:
                weather_icon = snowflake_symbol
            elif weather_id >= 801 and weather_id <= 804:
                weather_icon = cloud_symbol
            else:
                weather_icon = sun_symbol

            # Check for extreme temperatures and provide alerts
            extreme_temp_alert = ""
            if temperature < 0:
                extreme_temp_alert = f"{snowflake_symbol} **FREEZING ALERT**"
            elif temperature > 32:
                extreme_temp_alert = f"{sun_symbol} **HEATWAVE ALERT**"

            # Print the forecast details for each day
            print(
                f"Date: {date}, Temp: {temperature}°C, Wind Speed: {wind_speed} m/s, Humidity: {humidity}%, Weather: {weather_icon} {weather_description} {extreme_temp_alert}")
    else:
        print("Error retrieving 5-day forecast.")


if __name__ == "__main__":
    test_weather_service()
