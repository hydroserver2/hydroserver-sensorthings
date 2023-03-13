from ninja import Router, Query
from django.http import HttpResponse
from hydrothings.engine import SensorThingsRequest
from hydrothings.schemas import QueryParams
from hydrothings.utils import entity_or_404, entities_or_404, generate_response_codes, parse_query_params
from .schemas import SensorPostBody, SensorPatchBody, SensorListResponse, SensorGetResponse


router = Router(tags=['Sensors'])


@router.get(
    '/Sensors',
    response=generate_response_codes('list', SensorListResponse),
    by_alias=True,
    url_name='list_sensor',
    exclude_none=True
)
def list_sensors(request, params: QueryParams = Query(...)):
    """
    Get a collection of Sensor entities.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a>
    """

    response = request.engine.list(
        **parse_query_params(
            query_params=params.dict(),
            entity_chain=request.entity_chain
        )
    )
    return entities_or_404(response)


@router.get(
    '/Sensors({sensor_id})',
    response=generate_response_codes('get', SensorGetResponse),
    by_alias=True
)
def get_sensor(request, sensor_id: str):
    """
    Get a Sensor entity.

    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/properties" target="_blank">\
      Sensor Properties</a> -
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel/sensor/relations" target="_blank">\
      Sensor Relations</a>
    """

    response = request.engine.get(entity_id=sensor_id)

    return entity_or_404(response, sensor_id)


@router.post(
    '/Sensors',
    response=generate_response_codes('create')
)
def create_sensor(request: SensorThingsRequest, response: HttpResponse, sensor: SensorPostBody):
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

    sensor_id = request.engine.create(
        entity_body=sensor
    )

    response['location'] = request.engine.get_ref(
        entity_id=sensor_id
    )

    return 201, None


@router.patch(
    '/Sensors({sensor_id})',
    response=generate_response_codes('update')
)
def update_sensor(request: SensorThingsRequest, sensor_id: str, sensor: SensorPatchBody):
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

    request.engine.update(
        entity_id=sensor_id,
        entity_body=sensor
    )

    return 204, None


@router.delete(
    '/Sensors({sensor_id})',
    response=generate_response_codes('delete')
)
def delete_sensor(request, sensor_id: str):
    """
    Delete a Sensor entity.

    Links:
    <a href="http://www.opengis.net/spec/iot_sensing/1.1/req/create-update-delete/delete-entity" target="_blank">\
      Delete Entity</a>
    """

    request.engine.delete(
        entity_id=sensor_id
    )

    return 204, None
