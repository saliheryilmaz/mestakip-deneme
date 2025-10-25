web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn metis_admin.wsgi:application -c gunicorn.conf.py
