FROM python:3.9.5-slim

COPY boms /boms
COPY weather_station.py /

ENTRYPOINT /weather_station.py