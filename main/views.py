from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from datetime import date, datetime, timedelta

def index(request):
    print("constructor index")
    return render(request, 'main/index.html')

def get_future_dates():
    today = datetime.today()
    future_dates = [today + timedelta(days=i) for i in range(1, 8)]
    return future_dates

def get_weather_data(lat, lon):
    api_key = 'Type_your_API_Key'
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=imperial&exclude=minutely,hourly,alerts&appid={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

# @csrf_exempt
def get_weather(request):
    print("weather function called")
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        
        weather_data = get_weather_data(lat, lon)
        
        if weather_data:
            future_dates = get_future_dates()
            weather_info = {
                "Timezone": weather_data['timezone'],
                'time': datetime.utcfromtimestamp(weather_data['current']['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": str(weather_data['current']['temp']) + ' °F',
                "pressure": str(weather_data['current']['pressure']),
                "humidity": str(weather_data['current']['humidity']),
                'forecast': str(weather_data['current']['weather'][0]['main']),
                'information': str(weather_data['current']['weather'][0]['description']),
                'icon': weather_data['current']['weather'][0]['icon']
            }
            
            if weather_info['forecast'] == "Smoke":
                weather_info["image"] = "smoke.jpeg"
            elif weather_info['forecast'] == "Haze":
                weather_info["image"] = "haze.jpeg"
            elif weather_info['forecast'] == "Rain":
                weather_info["image"] = "rainy.jpeg"
            elif weather_info['forecast'] == "Clouds":
                weather_info["image"] = "cloudy.jpeg"
            elif weather_info['forecast'] == "Thunderstorm":
                weather_info["image"] = "thunder.jpeg"
            else:
                weather_info["image"] = "bgimage1.jpeg"
            
            daily_forecast = []
            for i, date in enumerate(future_dates):
                forecast = {
                    'temp_min': weather_data['daily'][i+1]['temp']['min'],
                    'temp_max': weather_data['daily'][i+1]['temp']['max'],
                    'humidity': weather_data['daily'][i+1]['humidity'],
                    'date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'pressure': weather_data['daily'][i+1]['pressure'],
                    'description': weather_data['daily'][i+1]['weather'][0]['description'],
                    'icon': weather_data['daily'][i+1]['weather'][0]['icon']
                }
                daily_forecast.append(forecast)
            
            weather_info["daily_forecast"] = daily_forecast
            print(weather_info)
            
            return JsonResponse(weather_info)
        else:
            error_response = {"error": "Weather data not available"}
            return JsonResponse(error_response, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
