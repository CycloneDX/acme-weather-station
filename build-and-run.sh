#!/usr/bin/env bash
set -e
./update-boms.sh
docker build --tag acme-weather-station .
docker run --env OPENWEATHER_API_KEY="$OPENWEATHER_API_KEY" --env OPENWEATHER_CITY_NAME="$OPENWEATHER_CITY_NAME" --tty --interactive --expose 8000 acme-weather-station