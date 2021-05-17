#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from threading import Thread, Event
import traceback
import urllib.error
import urllib.request


OPENWEATHER_CITY_NAME = 'London,uk'
OPENWEATHER_API_KEY = None

MEDIA_TYPE_XML = 'application/vnd.cyclonedx+xml'
MEDIA_TYPE_JSON = 'application/vnd.cyclonedx+json'
MEDIA_TYPE_PROTOBUF = 'application/x.vnd.cyclonedx+protobuf'
MEDIA_TYPE_SPDX = 'text/spdx'

media_type_extensions = {
    MEDIA_TYPE_XML: 'xml',
    MEDIA_TYPE_JSON: 'json',
    MEDIA_TYPE_SPDX: 'spdx',
}

cached_weather = {}


def get(url):
    try:
        url = urllib.request.urlopen(url)
        if url.getcode() == 200:
            return url.read()
        else:
            print('Error receiving data', url.getcode())
    except urllib.error.HTTPError as exc:
        print('Error receiving data, HTTP status code', exc.code, exc.msg)


def update_weather():
    global cached_weather
    while True:
        try:
            print('Fetching latest weather information for', OPENWEATHER_CITY_NAME)
            if OPENWEATHER_API_KEY:
                weather_json = get('https://api.openweathermap.org/data/2.5/weather?q=' + OPENWEATHER_CITY_NAME + '&APPID=' + OPENWEATHER_API_KEY)
                cached_weather = json.loads(weather_json)
                print('Latest weather information updated.')
            else:
                # this is a throw away request to simulate documented behaviour
                get('https://api.openweathermap.org/data/2.5/weather?q=' + OPENWEATHER_CITY_NAME)
                cached_weather = {
                    "coord": {
                        "lon": -122.08,
                        "lat": 37.39
                    },
                    "weather": [
                        {
                            "id": 800,
                            "main": "Clear",
                            "description": "clear sky",
                            "icon": "01d"
                        }
                    ],
                    "base": "stations",
                    "main": {
                        "temp": 282.55,
                        "feels_like": 281.86,
                        "temp_min": 280.37,
                        "temp_max": 284.26,
                        "pressure": 1023,
                        "humidity": 100
                    },
                    "visibility": 16093,
                    "wind": {
                        "speed": 1.5,
                        "deg": 350
                    },
                    "clouds": {
                        "all": 1
                    },
                    "dt": 1560350645,
                    "sys": {
                        "type": 1,
                        "id": 5122,
                        "message": 0.0139,
                        "country": "US",
                        "sunrise": 1560343627,
                        "sunset": 1560396563
                    },
                    "timezone": -25200,
                    "id": 420006353,
                    "name": "Mountain View",
                    "cod": 200
                }
                print('Using mocked weather information.')
        except Exception as exc:
            print('Error fetching latest weather information...')
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        Event().wait(30)


def undocumented_service_call():
    while True:
        try:
            print('Making an undocumented service call...')
            get('https://www.example.com')
            print('Undocumented service call made.')
        except Exception as exc:
            print('Error making undocumented service call...')
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        Event().wait(60)


class HTTPHandler(BaseHTTPRequestHandler):
    def content_negotiation(self):
        accepted_content_entries = self.headers['accept'].split(',')
        for accepted_content_entry in accepted_content_entries:
            print('Accept entry:', accepted_content_entry)
            media_type, _, parameters = accepted_content_entry.partition(';')
            media_type = media_type.strip()
            version = None

            if len(parameters.strip()):
                parameter_name, _, parameter_value = parameters.partition('=')
                if parameter_name.strip() == 'version':
                    version = parameter_value.strip()

            if media_type in media_type_extensions:
                return media_type, version
            elif media_type == '*/*':
                return MEDIA_TYPE_JSON, '1.3'

        print('Unable to negotiate content type')
        self.send_response(406, "Supported media types are " + ", ".join(media_type_extensions.keys()))

    def do_GET(self):
        if self.path == '/.well-known/sbom':
            self.send_response(307)
            self.send_header("Location", "/bom")
            self.end_headers()
        elif self.path == "/bom":
            media_type, version = self.content_negotiation()
            if media_type == MEDIA_TYPE_SPDX:
                version = '2.2'
            elif version is None:
                version = '1.3'
            filename = 'bom-' + version + '.' + media_type_extensions[media_type]
            print('Returning:', filename)

            content_type = media_type
            if media_type != MEDIA_TYPE_SPDX:
                content_type += '; version=' + version
            print('Content type:', content_type)

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()

            with open('boms/' + filename, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == "/weather":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(cached_weather).encode('UTF-8'))
        else:
            self.send_response(404)
            self.wfile.write('Hmmm.... maybe you\'re looking for "/.well-known/sbom", "/bom" or "/weather"?'.encode('UTF-8'))


def run(server_class=HTTPServer, handler_class=HTTPHandler):
    Thread(target=update_weather, daemon=True).start()
    Thread(target=undocumented_service_call, daemon=True).start()

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Starting server listening on port 8000...')
    httpd.serve_forever()


if __name__ == '__main__':
    if os.environ.get(OPENWEATHER_CITY_NAME, ''):
        OPENWEATHER_CITY_NAME = os.environ['OPENWEATHER_CITY_NAME']
    if 'OPENWEATHER_API_KEY' in os.environ:
        OPENWEATHER_API_KEY = os.environ['OPENWEATHER_API_KEY']

    run()
