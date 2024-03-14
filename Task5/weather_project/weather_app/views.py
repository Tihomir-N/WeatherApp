from django.shortcuts import render
import requests
import datetime
from .models import Weather
from django.http import JsonResponse

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
    GOOGLE_API_KEY = 'AIzaSyDeOG-bIle69JmMD7tulwLdOKgknRah2N4'
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

def find_coldest_city(cities):
    min_temp = float('inf')
    min_city = ''
    PARAMS = {'units':'metric'}

    for city in cities:
        url = build_request_url_openWeatherMap(city)
        _, _, temp = get_weather_data(url, PARAMS)

        if temp < min_temp:
            min_temp = temp
            min_city = city

    return min_city

def calculate_average_temperature(cities):
    total_temp = 0
    PARAMS = {'units':'metric'}

    for city in cities:
        url = build_request_url_openWeatherMap(city)
        _, _, temp = get_weather_data(url, PARAMS)

        total_temp += temp

    avg_temp = total_temp / len(cities)

    return round(avg_temp)

def get_recent_weather_stats():
    weather_data = Weather.objects.all()
    weather_data = weather_data.order_by('-date')[:10]
    return weather_data

def home(request):
    PARAMS = {'units':'metric'}
    city = request.POST.get('city') or request.GET.get('city', 'London') or 'London'
    url = build_request_url_openWeatherMap(city)
    
    description, icon, temp = get_weather_data(url, PARAMS)
    if description is None:
        description = 'Unknown'
        icon = 'unknown'
        temp = 0
    else:
        weather_info = Weather(city=city, description=description, icon=icon, temp=temp)
        weather_info.save()

    image_url = get_city_images(city)
    day = datetime.date.today()

    cities = ['London', 'Paris', 'Berlin', 'Madrid', 'Rome']
    avg_temp = calculate_average_temperature(cities)
    min_city = find_coldest_city(cities)
    recent_weather_stats = get_recent_weather_stats()

    if request.method == 'GET' and 'refresh' in request.GET:
        return JsonResponse({
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'recent_weather_stats': list(recent_weather_stats.values())
        })
    else:
        return render(request, 'weather_app/index.html',{
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
            'avg_temp': avg_temp,
            'min_city': min_city,
            'cities': cities,
            'recent_weather_stats': recent_weather_stats
        })
