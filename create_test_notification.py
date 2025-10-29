#!/usr/bin/env python
"""Test bildirimi oluştur"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from dashboard.models import Notification, Event
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Tüm kullanıcılar için test bildirimleri oluştur
users = User.objects.all()

for user in users:
    # Şu andan 1 dakika sonra için bildirim
    future_time = timezone.now() + timedelta(minutes=1)
    
    Notification.objects.create(
        title=f"Test Bildirimi - {user.username}",
        message=f"Merhaba {user.username}! Bu bir test bildirimidir. Bildirim sistemi çalışıyor! 🎉",
        type='info',
        status='pending',
        user=user,
        scheduled_time=future_time
    )
    
    print(f"✓ {user.username} için test bildirimi oluşturuldu (1 dakika sonra)")

# Ayrıca şu an için de bir bildirim oluştur
for user in users:
    Notification.objects.create(
        title=f"Anında Bildirim - {user.username}",
        message=f"Bu bildirim hemen görünmelidir! Takvim etkinliklerinizi kontrol edin. 📅",
        type='event_reminder',
        status='pending',
        user=user,
        scheduled_time=timezone.now()
    )
    
    print(f"✓ {user.username} için anında bildirim oluşturuldu")

print("\n✅ Test bildirimleri başarıyla oluşturuldu!")
print("🔔 Şimdi tarayıcıda bildirim ikonuna tıklayın ve bildirimleri görün.")
