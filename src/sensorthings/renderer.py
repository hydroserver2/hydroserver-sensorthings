from ninja.renderers import JSONRenderer


class SensorThingsRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        return getattr(
            request,
            'response_string',
            JSONRenderer.render(self, request, data, response_status=response_status)
        )
