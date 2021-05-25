# ACME Weather Station

A mock IOT weather station with support for BOM retrieval.

Please note: this is a basic example. The web server is not fully standards
compliant. It _should_ support most basic requests. If handling is
missing for any required functionality feel free to raise an issue, or,
even better, create a pull request :)

It supports BOM discovery and access via the well known URIs `/.well-known/sbom` and `/.well-known/sbom/base`.

**Please note:** there is an existing internet draft [draft-ietf-opsawg-sbom-access](https://datatracker.ietf.org/doc/html/draft-lear-opsawg-sbom-access-00).
At present, this service simply responds with a redirect to the BOM. This
may change in the future to match what the final standard specifies.

Alternatively, the BOM can be retrieved directly from `/bom`.

## Usage

Note: Docker is required.

The simplest way to use this is to clone the repository and run `build-and-run.sh`...

```
git clone https://github.com/CycloneDX/acme-weather-station.git
cd acme-weather-station
./build-and-run.sh
```

By default the service listens on port 8000. The `build-and-run.sh` script can
be modified to change this.

## Supported Media Types

CycloneDX XML, JSON and Protobuf media types are supported for BOM retrieval:

- `application/vnd.cyclonedx+xml`
- `application/vnd.cyclonedx+json`
- `application/x.vnd.cyclonedx+protobuf`

The version parameter is also supported to specify what CycloneDX specification
version you want to retrieve. By default, the latest supported version will be
returned.

For example, to request a v1.2 JSON BOM, use the following header:

```
Accept: application/vnd.cyclonedx+json; version=1.2
```

You can also retrieve the BOM in SPDX tag/value format by using the media type
`text/spdx`. The SPDX media type doesn't support a version parameter. Only v2.2 is returned.

Or, you can just specify `*/*` to retrieve the default, which, for this service,
is currently CycloneDX v1.3 JSON.

Browsers, by default, add `*/*` to the `Accept` header meaning you can also
just browse to the relevant URL. i.e. `http://localhost:8000/.well-known/sbom`

## Weather Information

Weather information is retrieved from the OpenWeather Map API. This API requires
an API key. If you don't provide an API key a mock response will be returned.

To provide an API key set the environment variable `OPENWEATHER_API_KEY`.

To override the default weather location, London, set the environment variable `OPENWEATHER_CITY_NAME`.

## Services

Services are supported in CycloneDX specification v1.2 onwards.

The OpenWeather Map API call, `https://api.openweathermap.org/data/2.5/weather`, is documented in the BOM.

However, there is an undocumented service call to `https://www.example.com`. This is an intentional omission for anyone testing network monitoring use cases.
