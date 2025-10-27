#!/bin/bash
set -e

echo "🚀 Starting Railway deployment..."

# Check if we're on Railway
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "🚂 Railway environment detected"
    
    # Run deployment script
    echo "📋 Running deployment checks..."
    python railway_deploy.py
    
    echo "🌐 Starting Gunicorn on PORT: ${PORT:-8000}"
    
    # Start Gunicorn with better error handling
    exec gunicorn metis_admin.wsgi:application \
        --bind "0.0.0.0:${PORT:-8000}" \
        --workers 2 \
        --timeout 120 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --access-logfile - \
        --error-logfile - \
        --log-level info \
        --capture-output \
        --enable-stdio-inheritance
else
    echo "🏠 Local environment detected"
    echo "📊 Running migrations..."
    python manage.py migrate --noinput
    
    echo "🌐 Starting development server"
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
fi

