# -*- coding: utf-8 -*-
import logging

from weather_service import dummy
from datetime import datetime
from flask import jsonify
import  urllib.request
import json

def parse_datetime(date, hour):
    """Convert the date and hour to datetime."""
    """ makes sense only to convert the hour + up cause its the weather forecast
       and we only want to look for the futute weather """
    hour_edit = int(hour)
    if 0<hour_edit<300:
          hour_edit = 300
    elif hour_edit>2100 or hour_edit==0:
         hour_edit = '0000'
    else:
         while hour_edit % 3 != 0:
            hour_edit += 100
    return datetime.strptime("{}-{}".format(date, hour_edit), '%Y%m%d-%H%M')



def fetch_forecast_data(city):
    """Recover the city's forecast for the next 5 days at three hour intervals.

    This should contact the weather service API to recover the listing for the
    given city.

    :param city: The city name e.g. london.

    :returns: A list of data points for the city.

    """
    appid = '41d977380eced67739c7327163d02e0c'
    url = 'http://api.openweathermap.org/data/2.5/forecast?q=%s&units=metric&mode=json&APPID=%s' % (city, appid)
    file = urllib.request.urlopen(url)
    before_list = file.read()
    data = json.loads(before_list.decode('utf-8'))
    weather_list = data['list']
    return weather_list



def find_forecast(forecasts, date_time):
    """Find the requested data point if it exists.
    """
    date_hour = str(date_time)
    for i in forecasts:
      for k,v in i.items():
        if v == date_hour:
          pre_des = i.get('weather')
          pre_rest = i.get('main')
          result = {
              'description' : pre_des[0].get('description'),
              'humidity' : pre_rest.get('humidity'),
              'pressure' : pre_rest.get('pressure'),
              'temperature': pre_rest.get('temp'),
             }
          return result
        else:
          result =  {
             "message": "No data for %s" %date_hour,
             "status": "error"
            }
    return result





def get_forecast(city, date, hour, field=None):
    """Record the data or a specific field in the weather data.
    """
    log = logging.getLogger(__name__)

    log.debug(
        'Getting forecast for city: {} date: {} hour: {}'.format(
            city, date, hour
        )
    )

    forecasts = fetch_forecast_data(city)
    date_time = parse_datetime(date, hour)
    forecast = find_forecast(forecasts, date_time)

    return jsonify(forecast)


def get_forecast_by_field(city, date, hour, field):
    """Record the data or a specific field in the weather data.
    """
    log = logging.getLogger(__name__)

    log.debug(
        'Getting forecast for city: {} date: {} hour: {}: field'.format(
            city, date, hour,field
        )
    )

    forecasts = fetch_forecast_data(city)
    date_time = parse_datetime(date, hour)
    forecast = find_forecast(forecasts, date_time)


    if forecast.get(field) is None:
        return jsonify(forecast)
    else:
         field_data = {

         field : forecast.get(field)
         }
         return jsonify(field_data)
