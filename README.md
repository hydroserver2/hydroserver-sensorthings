# Django HydroThings (WIP)

The Django HydroThings Python package is an extension that helps implement the OGC SensorThings API specification in Django. The package is primarily built on top of the  [Django Ninja REST Framework](https://github.com/vitalik/django-ninja).

## Installation

You can install Django HydroThings using pip:

```
pip install django-hydrothings
```

## Usage

To use Django HydroThings in your Django project, add the following line to your `MIDDLEWARE` setting:

```
MIDDLEWARE = [
	# ...
	'hydrothings.middleware.SensorThingsMiddleware',
	# ...
]
```

Then you may use a prebuilt API backend by adding one of the following to your `INSTALLED_APPS` setting:

```
INSTALLED_APPS = [
	# ...
	'hydrothings.backends.sensorthings',
	'hydrothings.backends.odm2',
	'hydrothings.backends.frostserver'
	# ...
]
```

Alternatively, you may initialize a custom SensorThings API using an existing backend as a template and adding it to your urls.py file:

```
from hydrothings import SensorThingsAPI

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

You may further customize your API instance by subclassing `hydrothings.SensorThingsAbstractEngine` to create your own SensorThings engine to pass to the API instance instead of an existing backend. This is useful if you want to map the SensorThings API endpoints to a custom database backend.

You can also modify specific SensorThings endpoints and components using `hydrothings.SensorThingsComponent` and `hydrothings.SensorThingsEndpoint` to add custom authorization rules, disable certain endpoints, or customize SensorThings properties schemas.

## Documentation

For detailed documentation on how to use Django HydroThings, please refer to the [official documentation]().

## License

Django HydroThings is licensed under the [MIT License](https://github.com/hydroserver2/django-hydrothings/blob/main/LICENSE.txt).