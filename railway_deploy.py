#!/usr/bin/env python
"""
Railway deployment script
Bu script Railway'de deployment sırasında çalışacak özel komutları içerir
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Django ayarlarını yükle"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
    django.setup()

def run_migrations():
    """Migration'ları çalıştır"""
    print("🔄 Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def create_superuser():
    """Superuser oluştur"""
    print("👤 Creating superuser...")
    try:
        execute_from_command_line(['manage.py', 'create_auto_superuser'])
        print("✅ Superuser created successfully")
        return True
    except Exception as e:
        print(f"⚠️ Superuser creation warning: {e}")
        return True  # Bu hata kritik değil

def collect_static():
    """Static dosyaları topla"""
    print("📁 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully")
        return True
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def check_database():
    """Database bağlantısını kontrol et"""
    print("🔍 Checking database connection...")
    try:
        from django.db import connection
        from django.conf import settings
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        
        # Database tipini kontrol et
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' in db_engine.lower():
            print("✅ PostgreSQL database kullanılıyor - Veriler kalıcı olacak")
        elif 'sqlite' in db_engine.lower():
            if os.environ.get('RAILWAY_ENVIRONMENT'):
                print("⚠️  WARNING: SQLite kullanılıyor - Veriler her deploy'da kaybolabilir!")
                print("⚠️  PostgreSQL database eklemenizi öneririz")
        
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Ana deployment fonksiyonu"""
    print("🚀 Starting Railway deployment process...")
    
    # Django'yu ayarla
    setup_django()
    
    # Database bağlantısını kontrol et
    if not check_database():
        print("❌ Database connection failed, exiting...")
        sys.exit(1)
    
    # Migration'ları çalıştır
    if not run_migrations():
        print("❌ Migrations failed, exiting...")
        sys.exit(1)
    
    # Superuser oluştur
    create_superuser()
    
    # Static dosyaları topla
    if not collect_static():
        print("❌ Static files collection failed, exiting...")
        sys.exit(1)
    
    print("✅ Railway deployment completed successfully!")

if __name__ == "__main__":
    main()