# Weather Microservice Communication Contract
This README provides the communication contract for the weather microservice that I implemented. It includes clear instructions for requesting and receiving data from the microservice, and a UML sequence diagram to illustrate the flow of communication.

Requesting Data from the Microservice:
To request data from the WeatherService, you can use the following HTTP GET requests. You need to call the API with the city name to retrieve the weather information.

Get Current Weather:

Endpoint: /weather

Method: GET

Parameters:

city_name (required): The name of the city you want to retrieve weather data for.
Example Call:

python
Copy code
import requests

city_name = "Seattle"
api_key = "your_api_key_here"
response = requests.get(f"http://yourdomain.com/weather?city_name={city_name}&appid={api_key}")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
Get 5-Day Weather Forecast:

Endpoint: /forecast

Method: GET

Parameters:

city_name (required): The name of the city you want to retrieve the forecast for.
Example Call:

python
Copy code
import requests

city_name = "Seattle"
api_key = "your_api_key_here"
response = requests.get(f"http://yourdomain.com/forecast?city_name={city_name}&appid={api_key}")

if response.status_code == 200:
    forecast = response.json()
    print(forecast)
else:
    print(f"Failed to retrieve data: {response.status_code}")
