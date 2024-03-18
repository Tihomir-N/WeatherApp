import tkinter as tk
import requests
import random

def get_weather(city):
    api_key = "22ef52c6707559f8d3fe948e2ef01fbb"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code != 200:
        return None

    weather = data['weather'][0]['main']
    temperature_k = data['main']['temp']
    temperature_c = round((temperature_k - 273.15), 1)
    humidity = data['main']['humidity']
    return weather, temperature_c, humidity

def fetch_weather():
    city = city_entry.get()
    result = get_weather(city)
    
    if result is None:
        weather_label.config(text="Please enter a valid city name.")
    else:
        weather, temperature_c, humidity = result
        weather_label.config(text=f"Weather in {city}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%")

def get_random_cities():
    api_url = 'https://api.api-ninjas.com/v1/city?min_population={}&limit=100'.format('1000000')
    response = requests.get(api_url, headers={'X-Api-Key': '8UbplA20/DRBsYdkZtz2sw==Lty5K8snkj93nyuo'})
    if response.status_code == requests.codes.ok:
        cities = response.json()
        return random.sample(cities, 5)
    else:
        print("Error:", response.status_code, response.text)

def show_random_cities():
    random_cities = get_random_cities()
    coldest_temp = float('inf')
    total_temp = 0

    cities_info = ""
    for city in random_cities:
        city_name = city['name']
        weather, temperature_c, humidity = get_weather(city_name)
        total_temp += temperature_c
        if temperature_c < coldest_temp:
            coldest_temp = temperature_c
            coldest_city = city_name
        cities_info += f"{city_name}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%\n"

    average_temp = total_temp / len(random_cities)
    random_cities_label.config(text=f"Coldest City: {coldest_city}, Coldest Temperature: {coldest_temp}°C\n"
                             f"Average Temperature of Random Cities: {average_temp:.1f}°C\n\n"
                             f"{cities_info}")

root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter city name:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=fetch_weather)
get_weather_button.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

random_cities_button = tk.Button(root, text="Show Random Cities", command=show_random_cities)
random_cities_button.pack()

random_cities_label = tk.Label(root, text="")
random_cities_label.pack()

root.mainloop()
