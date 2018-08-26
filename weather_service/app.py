
# -*- coding: utf-8 -*-
from flask import Flask
from weather_service import views
from weather_service.config import Configuration


def create_app():
    app = Flask(__name__)

    app.config.from_object(Configuration)

    app.url_map.strict_slashes = False

    app.register_blueprint(views.blueprint)

    return app
