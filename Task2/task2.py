import tkinter as tk
import requests

def get_weather(city):
    api_key = "22ef52c6707559f8d3fe948e2ef01fbb"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code != 200:
        return None

    weather = data['weather'][0]['main']
    temperature_k = data['main']['temp']
    temperature_c = round((temperature_k - 273.15),1)
    humidity = data['main']['humidity']
    return weather, temperature_c, humidity

def fetch_weather():
    city = city_entry.get()
    result = get_weather(city)
    
    if result is None:
        result_label.config(text=f"Please enter a valid city name.")
    else:
        weather, temperature_c, humidity = result
        result_label.config(text=f"Weather in {city}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%")

root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter city name:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=fetch_weather)
get_weather_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
