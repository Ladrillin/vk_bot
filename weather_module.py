import requests
import json
from datetime import datetime
from opencage.geocoder import OpenCageGeocode


def yandex_weather(place):
    geocoder_token = 'token'
    geocoder = OpenCageGeocode(geocoder_token)
    geocode_results = geocoder.geocode(str(place))
    latitude = str('%6f' % geocode_results[0]['geometry']['lat'])
    longitude = str('%6f' % geocode_results[0]['geometry']['lng'])  # %6f Яндекс предпочитает 6 знаков после запятой
    print(geocode_results[0]['geometry']['lat'],
          geocode_results[0]['geometry']['lng'])

    url = f'https://api.weather.yandex.ru/v2/informers?lat={latitude}&lon={longitude}'
    query_headers = {
        'X-Yandex-API-Key': 'token'
    }
    response_yandex = requests.get(url, headers=query_headers)
    return response_yandex.json()


def weather_formatting(weather_json):
    timestamp = weather_json['fact']['obs_time']  # + (60*60*3)  # UTC + 3; obs - observation
    from_time_stamp = datetime.fromtimestamp(timestamp)  # Отдельно от других параметров считается время
    yandex_obs_time = (datetime.strftime(from_time_stamp, '%Y-%m-%d %H:%M')[11::])  # Вывод только часа и минуты
    yandex_weather_data = {
        'yandex_temp': weather_json['fact']['temp'],
        'yandex_feels_like': weather_json['fact']['feels_like'],
        'yandex_wind_speed': weather_json['fact']['wind_speed'],
        'yandex_pressure_mm': weather_json['fact']['pressure_mm'],
        'yandex_humidity': weather_json['fact']['humidity'],
        'yandex_wind_gust': weather_json['fact']['wind_gust'],
        'yandex_obs_time': yandex_obs_time,
    }
    return yandex_weather_data


def weather_info_text(params):
    weather_info = str(f'Температура {params["yandex_temp"]}°\n'
                       f'Ощущается как {params["yandex_feels_like"]}°\n'
                       f'Скорость ветра {params["yandex_wind_speed"]} м/с\n'
                       f'Порывы ветра до {params["yandex_wind_gust"]} м/c\n'
                       f'Давление {params["yandex_pressure_mm"]} мм\n'
                       f'Влажность воздуха {params["yandex_humidity"]}%\n'
                       f'Данные представлены на момент {params["yandex_obs_time"]} по московскому времени\n\n'
                       )
    return weather_info


def followup_weather(weather_json):
    followup_weather_data = {
        'followup_temp': weather_json['forecast']['parts'][0]['temp_avg'],
        'followup_feels_like': weather_json['forecast']['parts'][0]['feels_like'],
        'followup_wind_speed': weather_json['forecast']['parts'][0]['wind_speed'],
        'followup_wind_gust': weather_json['forecast']['parts'][0]['wind_gust'],
        'followup_humidity': weather_json['forecast']['parts'][0]['humidity']
    }
