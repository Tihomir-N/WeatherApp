from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'New York'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=45f233f948350a497d03aead20ce1b0d'
    PARAMS = {'units':'metric'}

    API_KEY = 'AIzaSyAJblJzsRsFl3VeetqLfjr7sEv9mkVc8n4'
    SEARCH_ENGINE_ID = '9732b7cac993c4c82'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get('items')
    image_url = search_items[1]['link']
    
    try:
        data = requests.get(url,params=PARAMS).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()

        return render(request, 'weather_app/index.html',{'description':description,'icon':icon,'temp':temp,'day':day,'city':city,"exception_occurred":False,'image_url':image_url})
    
    except:
        exception_occurred=True
        messages.error(request, 'Please enter a valid city name.')
        day=datetime.date.today()

        return render(request, 'weather_app/index.html',{'description':'clear sky','icon':'01d','temp':25,'day':day,'city':'New York',"exception_occurred":True})
    

