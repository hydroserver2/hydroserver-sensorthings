# HydroServer SensorThings

The HydroServer SensorThings Python package is an extension that helps implement the OGC SensorThings API specification in Django. The package is primarily built on top of the  [Django Ninja REST Framework](https://github.com/vitalik/django-ninja).

## Installation

You can install HydroServer SensorThings using pip:

```
pip install hydroserver-sensorthings
```

## Usage

To use HydroServer SensorThings in your Django project, add the following line to your `MIDDLEWARE` setting:

```
MIDDLEWARE = [
	# ...
	'sensorthings.middleware.SensorThingsMiddleware',
	# ...
]
```

You may initialize a custom SensorThings API using an existing backend as a template and adding it to your urls.py file:

```
from sensorthings import SensorThingsAPI

# ...

my_st_api = SensorThingsAPI(
	title='My Custom SensorThings API',
	description='A custom SensorThings API for my Django project.',
	version='1.1',
	backend='sensorthings'
)

# ...

urlpatterns = [
	# ...
	path('v1.1/', my_st_api.urls),
	# ...
]
```

You may further customize your API instance by subclassing `sensorthings.SensorThingsAbstractEngine` to create your own SensorThings engine to pass to the API instance instead of an existing backend. This is useful if you want to map the SensorThings API endpoints to a custom database backend.

You can also modify specific SensorThings endpoints and components using `sensorthings.SensorThingsComponent` and `sensorthings.SensorThingsEndpoint` to add custom authorization rules, disable certain endpoints, or customize SensorThings properties schemas.

## Documentation

For detailed documentation on how to use HydroServer SensorThings, please refer to the [official documentation](https://hydroserver2.github.io/hydroserver-sensorthings/).

## Funding and Acknowledgements

Funding for this project was provided by the National Oceanic & Atmospheric Administration (NOAA), awarded to the Cooperative Institute for Research to Operations in Hydrology (CIROH) through the NOAA Cooperative Agreement with The University of Alabama (NA22NWS4320003).
