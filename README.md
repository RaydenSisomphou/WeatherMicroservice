# Weather Microservice Communication Contract
This README provides the communication contract for the weather microservice that I implemented. It includes clear instructions for requesting and receiving data from the microservice, and a UML sequence diagram to illustrate the flow of communication.

# Requesting Data from the Microservice:
To request data from the WeatherService, you can use the following HTTP GET requests. You need to call the API with the city name to retrieve the weather information.

## Get Current Weather:

Endpoint: (https://api.openweathermap.org/data/2.5/weather)
Method: GET
Parameters: city_name (required): The name of the city you want to retrieve weather data for.
Example Call:
```python
import requests

city_name = "Seattle"
api_key = "your_api_key_here"
response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
```

## Get 5-Day Weather Forecast:

Endpoint: /forecast
Method: GET
Parameters:city_name (required): The name of the city you want to retrieve the forecast for.
Example Call:
```python 
import requests

city_name = "Seattle"
api_key = "your_api_key_here"
response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}")

if response.status_code == 200:
    forecast = response.json()
    print(forecast)
else:
    print(f"Failed to retrieve data: {response.status_code}")
```
# Receiving Data from the Microservice:

Responses are in JSON format. 

## Receive Current Weather 
```python
{
  "main": {
    "temp": 15.5,
    "humidity": 82
  },
  "weather": [
    {
      "description": "light rain"
    }
  ],
  "wind": {
    "speed": 4.1
  }
}
```

## Receive 5-Day Weather Forecast 
```python
{
  "list": [
    {
      "dt": 1697635200,
      "main": {
        "temp": 14.0
      },
      "weather": [
        {
          "description": "clear sky"
        }
      ]
    },
    {
      "dt": 1697721600,
      "main": {
        "temp": 16.0
      },
      "weather": [
        {
          "description": "few clouds"
        }
      ]
    }
  ]
}
```

# UML Sequence Diagram
