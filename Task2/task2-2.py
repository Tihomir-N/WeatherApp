from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
import sys
import requests
import random

def get_random_cities():
    api_url = 'https://api.api-ninjas.com/v1/city?min_population={}&limit=100'.format('1000000')
    response = requests.get(api_url, headers={'X-Api-Key': '8UbplA20/DRBsYdkZtz2sw==Lty5K8snkj93nyuo'})
    if response.status_code == requests.codes.ok:
        cities = response.json()
        return random.sample(cities, 5)
    else:
        print("Error:", response.status_code, response.text)

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

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.city_label = QLabel('Enter city name:', self)
        self.city_entry = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.result_label = QLabel('', self)

        self.random_cities_button = QPushButton('Show Random Cities', self)
        self.random_cities_label = QLabel('', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_entry)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.random_cities_button)
        vbox.addWidget(self.random_cities_label)

        self.setLayout(vbox)

        self.get_weather_button.clicked.connect(self.fetch_weather)
        self.random_cities_button.clicked.connect(self.show_random_cities)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Weather App')
        self.show()

    def fetch_weather(self):
        city = self.city_entry.text()
        result = get_weather(city)
        
        if result is None:
            QMessageBox.critical(self, "Error", "Please enter a valid city name.".format(city))
        else:
            weather, temperature_c, humidity = result
            self.result_label.setText(f"Weather in {city}: {weather}, Temperature: {temperature_c}°C, Humidity: {humidity}%")

    def show_random_cities(self):
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
        self.random_cities_label.setText(f"Coldest City: {coldest_city}, Coldest Temperature: {coldest_temp}°C\n"
                                         f"Average Temperature of Random Cities: {average_temp:.1f}°C\n\n"
                                         f"{cities_info}")

app = QApplication(sys.argv)
ex = WeatherApp()
sys.exit(app.exec_())
