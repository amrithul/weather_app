import datetime
from django.shortcuts import render
import json
import urllib.request

def index(request):
    data = {}  # Default empty dictionary to avoid errors if GET request
    if request.method == 'POST':
        city = request.POST.get('city', '')  # Retrieve city name from form
        try:
            # Fetch JSON data from the OpenWeatherMap API
            source = urllib.request.urlopen(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=d07d0092e5f02d2b6e7888de9419974a&units=metric'
            ).read()
            list_of_data = json.loads(source)
            
            # Populate weather data into the dictionary
            data = {
                "city_name": list_of_data['name'],
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": f"{list_of_data['coord']['lon']} {list_of_data['coord']['lat']}",
                "temp": f"{list_of_data['main']['temp']} °C",
                "feels_like": f"{list_of_data['main']['feels_like']} °C",
                "temp_min": f"{list_of_data['main']['temp_min']} °C",
                "temp_max": f"{list_of_data['main']['temp_max']} °C",
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "weather": list_of_data['weather'][0]['main'],
                "weather_description": list_of_data['weather'][0]['description'],
                "wind_speed": f"{list_of_data['wind']['speed']} m/s",
                "wind_deg": f"{list_of_data['wind']['deg']}°",
                "cloudiness": f"{list_of_data['clouds']['all']}%",
                "sunrise": (datetime.datetime.fromtimestamp(list_of_data['sys']['sunrise']) + datetime.timedelta(hours=5, minutes=30)).strftime('%H:%M:%S'),
                "sunset": (datetime.datetime.fromtimestamp(list_of_data['sys']['sunset']) + datetime.timedelta(hours=5, minutes=30)).strftime('%H:%M:%S'),
            }
        except Exception as e:
            data = {"error": "City not found. Please enter a valid city name."}

    return render(request, "index.html", {"data": data})

