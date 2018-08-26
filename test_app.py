import pytest
from flask import url_for,jsonify
from weather_service import backend

class TestApp:

    def test_get_complete_forecast(self,client):
        result = client.get('/london/20180827/2000')
        test_result = backend.get_forecast('london','20180827','2000')
        assert result.status_code == 200
        assert result.json == test_result.json

    def test_get_complete_forecast_by_field(self,client):
        result = client.get('/London/20180829/0600/humidity')
        test_result = backend.get_forecast_by_field('London','20180829','0600','humidity')
        assert result.status_code == 200
        assert result.json == test_result.json

    def test_ping(self,client):
        result = client.get('/')
        assert result.status_code == 200
        message = jsonify(
            dict(
                status="ok",
                name="weatherservice",
                version=open('VERSION').read().strip(),
            )
            )
        assert result.json == message.json
