"""
Healthcheck endpoint for Railway deployment
"""
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def healthcheck(request):
    """
    Simple healthcheck endpoint that returns 200 OK
    """
    return HttpResponse("OK", status=200)
