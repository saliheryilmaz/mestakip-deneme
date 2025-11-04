#!/usr/bin/env python
import os
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import UserProfile

def update_admin_role():
    """Admin kullanıcısının rolünü kesin olarak admin yap"""
    try:
        # Admin kullanıcısını bul
        admin_user = User.objects.get(username='admin')
        
        # Profili al veya oluştur
        profile, created = UserProfile.objects.get_or_create(user=admin_user)
        
        # Rolü admin yap
        profile.role = 'admin'
        profile.save()
        
        print(f"✅ Admin kullanıcısı güncellendi:")
        print(f"   Kullanıcı: {admin_user.username}")
        print(f"   Rol: {profile.role}")
        print(f"   Display: {profile.get_role_display()}")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Admin kullanıcısı bulunamadı")
        return False
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    update_admin_role()