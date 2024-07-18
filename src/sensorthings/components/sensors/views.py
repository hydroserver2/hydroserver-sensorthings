from ninja import Query
from django.http import HttpResponse
from sensorthings import settings
from sensorthings.router import SensorThingsRouter
from sensorthings.http import SensorThingsHttpRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import Sensor, SensorPostBody, SensorPatchBody, SensorListResponse, SensorGetResponse


router = SensorThingsRouter(tags=['Sensors'])
id_qualifier = settings.ST_API_ID_QUALIFIER
id_type = settings.ST_API_ID_TYPE


@router.st_list('/Sensors', response_schema=SensorListResponse, url_name='list_sensor')
def list_sensors(
        request,
        params: ListQueryParams = Query(...)
):
    """
    Get a collection of Sensor entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a>
    """

    return request.engine.list_entities(
        component=Sensor,
        query_params=params.dict()
    )


@router.st_get(f'/Sensors({id_qualifier}{{sensor_id}}{id_qualifier})', response_schema=SensorGetResponse)
def get_sensor(
        request: SensorThingsHttpRequest,
        sensor_id: id_type,
        params: GetQueryParams = Query(...)
):
    """
    Get a Sensor entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a>
    """

    return request.engine.get_entity(
        component=Sensor,
        entity_id=sensor_id,
        query_params=params.dict()
    )


@router.st_post('/Sensors')
def create_sensor(
        request: SensorThingsHttpRequest,
        response: HttpResponse,
        sensor: SensorPostBody
):
    """
    Create a new Sensor entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/create-entity" target="_blank">\
      Create Entity</a>
    """

    request.engine.create_entity(
        component=Sensor,
        entity_body=sensor,
        response=response
    )

    return 201, None


@router.patch(f'/Sensors({id_qualifier}{{sensor_id}}{id_qualifier})')
def update_sensor(
        request: SensorThingsHttpRequest,
        sensor_id: id_type,
        sensor: SensorPatchBody
):
    """
    Update an existing Sensor entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/update-entity" target="_blank">\
      Update Entity</a>
    """

    request.engine.update_entity(
        component=Sensor,
        entity_id=sensor_id,
        entity_body=sensor
    )

    return 204, None


@router.delete(f'/Sensors({id_qualifier}{{sensor_id}}{id_qualifier})')
def delete_sensor(
        request: SensorThingsHttpRequest,
        sensor_id: id_type
):
    """
    Delete a Sensor entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete_entity(
        component=Sensor,
        entity_id=sensor_id
    )

    return 204, None
