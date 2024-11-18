from weather_service import WeatherService
from datetime import datetime, timezone


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

    # Step 3: Ask if user wants current weather or 5-day forecast
    print("\n1. Current Weather")
    print("2. 5 Day Forecast")
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
        # Get 5-day forecast
        forecast = weather_service.get_5_day_forecast(lat, lon)

        if forecast:
            print(f"\n5-Day Forecast for {city_name}:")
            for day in forecast:
                time = day['dt']  # Timestamp in seconds
                temperature = day['temp']
                weather_description = day['weather']

                # Convert timestamp to readable date
                date = datetime.fromtimestamp(time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

                print(f"Date: {date}, Temp: {temperature}°C, Weather: {weather_description}")
        else:
            print("Error retrieving forecast data.")

    else:
        print("Invalid choice. Please enter 1 or 2.")


# Run
if __name__ == "__main__":
    test_weather_service()
# v2.0