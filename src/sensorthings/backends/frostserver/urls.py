from django.urls import path
from sensorthings import SensorThingsAPI


sensorthings_api_1_1 = SensorThingsAPI(
    version='1.1',
    backend='frostserver'
)

sensorthings_api_1_0 = SensorThingsAPI(
    version='1.0',
    backend='frostserver'
)

urlpatterns = [
    path('v1.0/', sensorthings_api_1_0.urls),
    path('v1.1/', sensorthings_api_1_1.urls)
]
