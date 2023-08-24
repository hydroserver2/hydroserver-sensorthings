from ninja import Router
from django.urls import reverse
from .schemas import ServerRootResponse
from sensorthings import settings


router = Router()


@router.get(
    '',
    include_in_schema=False,
    by_alias=True,
    response=ServerRootResponse
)
def get_root(request):
    """
    Get SensorThings server capabilities.
    """

    host_url = request.get_host()
    response = {
        'server_settings': {
            'conformance': settings.ST_CONFORMANCE
        },
        'server_capabilities': [
            {
                'name': capability['NAME'],
                'url': host_url + reverse(f"api-{settings.ST_VERSION}:{capability['VIEW']}")
            } for capability in settings.ST_CAPABILITIES
        ]
    }

    return response
