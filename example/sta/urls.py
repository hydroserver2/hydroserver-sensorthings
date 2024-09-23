from django.urls import path
from sensorthings import SensorThingsAPI
from sensorthings.extensions.dataarray import data_array_extension
from .engine import TestSensorThingsEngine, TestDataArraySensorThingsEngine


sta_core = SensorThingsAPI(
    title='Test SensorThings Core API',
    version='1.1',
    urls_namespace='core',
    description='This is a test SensorThings API.',
    engine=TestSensorThingsEngine
)

sta_data_array = SensorThingsAPI(
    title='Test SensorThings Data Array API',
    version='1.1',
    urls_namespace='da',
    description='This is a test SensorThings API.',
    engine=TestDataArraySensorThingsEngine,
    extensions=[data_array_extension]
)


urlpatterns = [
    path('core/v1.1/', sta_core.urls),
    path('data-array/v1.1/', sta_data_array.urls),
]
