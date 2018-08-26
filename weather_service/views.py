# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify,make_response
import os
from weather_service import backend

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
@blueprint.route('/ping')
def ping():
    """This is used to 'ping' the web service to check if its running.

    :returns: a status dict which the configured view will return as JSON.

    The dict has the form::

        dict(
            status="ok",
            name="weather-service",
            version="<version number of service>"
        )

    """
    if 'NO_AUTH_FOR_TEST' in os.environ:
           env_var = os.environ['NO_AUTH_FOR_TEST']

           test_var = authenticate(env_var)

           if test_var == True:
               return jsonify(
                   dict(
                       status="ok",
                       name="weatherservice",
                       version=open('VERSION').read().strip(),
                   )
                   )
           else:
                message = {
                  'error': 'You are not authorized'}
                return make_response(jsonify(message),401)
    else:
             message = {
                'error': 'Set the Enviroment variable NO_AUTH_FOR_TEST for authorization'
                }
             return make_response(jsonify(message),401)




def authenticate(variable):
    if variable == '1':
        return True
    else:
         return False


@blueprint.route('/<city>/<date>/<hour>', methods=['GET'])
def get_complete_forecast(city, date, hour):
    """Recover the complete dataset returned or handle no data found.
    """

    if 'NO_AUTH_FOR_TEST' in os.environ:
       env_var = os.environ['NO_AUTH_FOR_TEST']

       test_var = authenticate(env_var)

       if test_var == True:
          data = backend.get_forecast(city, date, hour)
          return make_response(data,200)
       else:
          message = {
            'error': 'You are not authorized'}
          return make_response(jsonify(message),401)
    else:
       message = {
          'error': 'Set the Enviroment variable NO_AUTH_FOR_TEST for authorization'
          }
       return make_response(jsonify(message),401)


@blueprint.route('/<city>/<date>/<hour>/<field>', methods=['GET'])
def get_complete_forecast_by_field(city, date, hour,field):
    """Recover the complete dataset returned or handle no data found.
    """
    if 'NO_AUTH_FOR_TEST' in os.environ:
           env_var = os.environ['NO_AUTH_FOR_TEST']
           test_var = authenticate(env_var)
           if test_var == True:
               data=backend.get_forecast_by_field(city, date, hour,field)
               return make_response(data)
           else:
               message = {
                 'error': 'You are not authorized'}
               return make_response(jsonify(message),401)
    else:
         message = {
            'error': 'Set the Enviroment variable NO_AUTH_FOR_TEST for authorization'
            }
         return make_response(jsonify(message),401)
