from ninja.renderers import BaseRenderer
from django.http import HttpRequest
from typing import Any


class FrostServerRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any = None, *, response_status: int) -> Any:
        return request
