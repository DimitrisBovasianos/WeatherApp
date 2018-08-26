

# -*- coding: utf-8 -*-
from weather_service.app import create_app
from flask import jsonify,make_response
import os

app = create_app()
