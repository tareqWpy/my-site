from django.conf import settings
from django.shortcuts import redirect, reverse


# ! for the MAINTANANCE_MODE
class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get("PATH_INFO", "")

        if settings.MAINTANANCE_MODE and path != reverse("maintenance"):
            response = redirect(reverse("maintenance"))
            return response

        response = self.get_response(request)

        return response
