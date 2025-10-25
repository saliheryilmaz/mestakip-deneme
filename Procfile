web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn metis_admin.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --max-requests 1000
