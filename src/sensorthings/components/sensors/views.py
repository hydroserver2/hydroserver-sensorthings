from ninja import Query
from sensorthings.router import SensorThingsRouter
from sensorthings.engine import SensorThingsRequest
from sensorthings.schemas import ListQueryParams, GetQueryParams
from .schemas import SensorPostBody, SensorPatchBody, SensorListResponse, SensorGetResponse


router = SensorThingsRouter(tags=['Sensors'])


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
        request=request,
        query_params=params.dict()
    )


@router.st_get('/Sensors({sensor_id})', response_schema=SensorGetResponse)
def get_sensor(
        request: SensorThingsRequest,
        sensor_id: str,
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
        request=request,
        entity_id=sensor_id,
        query_params=params.dict()
    )


@router.st_post('/Sensors')
def create_sensor(
        request: SensorThingsRequest,
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

    return request.engine.create_entity(
        request=request,
        entity_body=sensor
    )


@router.patch('/Sensors({sensor_id})')
def update_sensor(
        request: SensorThingsRequest,
        sensor_id: str,
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

    return request.engine.update_entity(
        request=request,
        entity_id=sensor_id,
        entity_body=sensor
    )


@router.delete('/Sensors({sensor_id})')
def delete_sensor(
        request: SensorThingsRequest,
        sensor_id: str
):
    """
    Delete a Sensor entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    return request.engine.delete_entity(
        request=request,
        entity_id=sensor_id
    )
