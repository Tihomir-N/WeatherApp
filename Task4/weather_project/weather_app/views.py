from django.shortcuts import render
import requests
import datetime

def get_weather_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        return description, icon, temp
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None

def get_city_images(city):
    GOOGLE_API_KEY = 'AIzaSyA0GHHkjzqWHzBsIAA46m9QBavwd0HbS64'
    SEARCH_ENGINE_ID = '9732b7cac993c4c82'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_google_search_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    search_data = requests.get(city_google_search_url).json()
    search_items = search_data.get('items')
    if search_items:
        return search_items[0]['link']
    else:
        return None

def build_request_url_openWeatherMap(city):
    return f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=45f233f948350a497d03aead20ce1b0d'

def home(request):
    PARAMS = {'units':'metric'}
    city = request.POST.get('city', 'London')
    url = build_request_url_openWeatherMap(city)
    
    description, icon, temp = get_weather_data(url, PARAMS)
    if description is None:
        description = 'Unknown'
        icon = 'unknown'
        temp = 0

    image_url = get_city_images(city)
    day = datetime.date.today()

    return render(request, 'weather_app/index.html',{
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'image_url': image_url
    })