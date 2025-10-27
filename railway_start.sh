#!/bin/bash
set -e

echo "🚀 Starting Railway deployment..."

# Check if we're on Railway
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "🚂 Railway environment detected"
    echo "📊 Running migrations..."
    python manage.py migrate --noinput || echo "⚠️  Migration warning (continuing anyway)"
    
    echo "👤 Creating auto superuser if needed..."
    python manage.py create_auto_superuser
    
    echo "✅ Migrations completed"
    echo "🌐 Starting Gunicorn on PORT: ${PORT:-8000}"
    
    # Start Gunicorn
    exec gunicorn metis_admin.wsgi:application \
        --bind "0.0.0.0:${PORT:-8000}" \
        --workers 2 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
else
    echo "🏠 Local environment detected"
    echo "📊 Running migrations..."
    python manage.py migrate --noinput
    
    echo "🌐 Starting development server"
    exec python manage.py runserver 0.0.0.0:${PORT:-8000}
fi

