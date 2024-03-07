import requests

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

cities = ["Sofia", "London", "New York", "Tokyo", "Sydney"]
weather_data = {}

for city in cities:
    result = get_weather(city)
    if result is not None:
        weather, temperature_c, humidity = result
        weather_data[city] = [weather, temperature_c, humidity]

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
