from django.urls import path
from sensorthings import SensorThingsAPI


st_api = SensorThingsAPI(
    backend='sensorthings',
    version='1.1',
)

urlpatterns = [
    path('v1.1/', st_api.urls),
]
