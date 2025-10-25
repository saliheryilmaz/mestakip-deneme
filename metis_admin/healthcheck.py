"""
Healthcheck endpoint for Railway deployment
"""
from django.http import HttpResponse


def healthcheck(request):
    """
    Simple healthcheck endpoint that returns 200 OK
    """
    return HttpResponse("OK", status=200)
