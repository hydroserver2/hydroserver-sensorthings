from django.urls import path
from django.conf import settings
from hydrothings import SensorThingsAPI

print(dir(settings))


hydrothings_api_1_1 = SensorThingsAPI(
    version='1.1'
)

hydrothings_api_1_0 = SensorThingsAPI(
    version='1.0'
)

urlpatterns = [
    path('v1.0/', hydrothings_api_1_0.urls),
    path('v1.1/', hydrothings_api_1_1.urls)
]
