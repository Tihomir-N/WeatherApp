import requests
import random

def get_random_cities():
    api_url = 'https://api.api-ninjas.com/v1/city?min_population={}&limit=100'.format('1000000')
    response = requests.get(api_url, headers={'X-Api-Key': '8UbplA20/DRBsYdkZtz2sw==Lty5K8snkj93nyuo'})
    if response.status_code == requests.codes.ok:
        cities = response.json()
        return random.sample([city["name"] for city in cities], 5)
    else:
        print("Error:", response.status_code, response.text)

def get_weather(city):
    api_key = "22ef52c6707559f8d3fe948e2ef01fbb"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data['cod'] == '404':
        print('City not found')
        return None
    else:
        weather = data['weather'][0]['main']
        temperature_k = data['main']['temp']
        temperature_c = round((temperature_k - 273.15),1)
        humidity = data['main']['humidity']
        return weather, temperature_c, humidity

cities = []

def get_random_cities_weather(num_cities=5):
    random_cities = get_random_cities()
    weather_data = {}
    for city in random_cities:
        result = get_weather(city)
        if result is not None:
            weather, temperature_c, humidity = result
            weather_data[city] = [weather, temperature_c, humidity]
            print(f"Weather in {city}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%")
    return weather_data
weather_data = get_random_cities_weather(5)

coldest_city = min(weather_data, key=lambda x: weather_data[x][1])
avg_temperature = round(sum([data[1] for data in weather_data.values()]) / len(weather_data),1)

print(f"Coldest City: {coldest_city}")
print(f"Average Temperature: {avg_temperature}°C")

city = input("Enter city name: ")
result = get_weather(city)
if result is not None:
    weather, temperature_c, humidity = result
    print(f"Weather in {city}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%")
else:
    print(f"No data available for {city}.")
