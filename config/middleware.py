from typing import Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from django.http import HttpResponse, HttpRequest
from django.utils import timezone


class TimeZoneMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tzname = request.COOKIES.get("user_timezone")
        if tzname:
            try:
                timezone.activate(ZoneInfo(tzname))
            except ZoneInfoNotFoundError:
                timezone.deactivate()
        else:
            timezone.deactivate()

        return self.get_response(request)

