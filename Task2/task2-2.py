from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
import sys
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

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.city_label = QLabel('Enter city name:', self)
        self.city_entry = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.result_label = QLabel('', self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_entry)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.result_label)

        self.setLayout(vbox)

        self.get_weather_button.clicked.connect(self.fetch_weather)

        self.setGeometry(300, 300, 300, 200)
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

app = QApplication(sys.argv)
ex = WeatherApp()
sys.exit(app.exec_())