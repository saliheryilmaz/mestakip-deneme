#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from django.db import connection

# Migration tablosuna 0016'yı ekle
cursor = connection.cursor()
try:
    cursor.execute("""
        INSERT INTO django_migrations (app, name, applied) 
        VALUES ('dashboard', '0016_railway_fix', datetime('now'))
    """)
    print("Migration 0016_railway_fix başarıyla eklendi")
except Exception as e:
    print(f"Hata: {e}")
    # Zaten varsa sorun yok
    pass

cursor.close()