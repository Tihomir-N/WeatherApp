from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

def convert_to_celsius(temp_k):
    return round(temp_k - 273.15)

def get_weather_icon_url(weather):
    return f"https://openweathermap.org/img/wn/{weather}@4x.png"

def get_weather(city):
    api_key = "22ef52c6707559f8d3fe948e2ef01fbb"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return None

    data = response.json()
    weather = data['weather'][0]['main']
    temperature_k = data['main']['temp']
    temperature_c = convert_to_celsius(temperature_k)
    temp_min = convert_to_celsius(data['main']['temp_min'])
    temp_max = convert_to_celsius(data['main']['temp_max'])
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind = data['wind']['speed']
    feels_like = data['main']['feels_like']
    icon_url = get_weather_icon_url(data['weather'][0]['icon'])
    
    return weather, temperature_c, humidity, temp_min, temp_max, icon_url, pressure, wind, feels_like

@app.route('/', methods=['GET', 'POST'])
@app.route('/weather/<city>', methods=['GET', 'POST'])
def weather(city=None):
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            return redirect(f'/weather/{city}')
        else:
            error = "Please enter a city name."

    if city:
        result = get_weather(city)
        if result is None:
            error = "Please enter a valid city name."
        else:
            weather, temperature_c, humidity, temp_min, temp_max, icon_url, pressure, wind, feels_like = result
            return render_template('index.html', city=city, weather=weather, temperature_c=temperature_c, humidity=humidity, temp_min=temp_min, temp_max=temp_max, icon_url=icon_url, wind=wind, pressure=pressure, feels_like=feels_like)

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
