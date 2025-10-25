"""
Healthcheck endpoint for Railway deployment
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt
@require_http_methods(["GET"])
def healthcheck(request):
    """
    Simple healthcheck endpoint that returns 200 OK
    """
    try:
        # Check if we can access basic Django functionality
        from django.conf import settings
        
        return JsonResponse({
            'status': 'healthy',
            'message': 'Django application is running',
            'debug': settings.DEBUG,
            'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'unknown')
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'message': str(e)
        }, status=500)
