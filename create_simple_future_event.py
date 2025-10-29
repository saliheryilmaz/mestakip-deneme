#!/usr/bin/env python
"""Basit gelecek tarihli test etkinliği oluştur"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from dashboard.models import Event, Notification
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime, date, time
import json

# Kullanıcıyı al (erhan kullanıcısı)
try:
    user = User.objects.get(username='erhan')
except User.DoesNotExist:
    print("❌ 'erhan' kullanıcısı bulunamadı!")
    exit(1)

# Bugünün tarihi
today = date.today()

# 2 saat sonrası için saat hesapla
now = datetime.now()
future_time = now + timedelta(hours=2)
event_time = time(hour=future_time.hour, minute=future_time.minute)

print(f"Bugünün tarihi: {today}")
print(f"Etkinlik saati: {event_time}")

# Etkinlik oluştur
event = Event.objects.create(
    title="Gelecek Toplantı",
    description="Bu toplantı 2 saat sonra başlayacak. Bildirimler 15 ve 5 dakika önce gelecek.",
    type='meeting',
    priority='high',
    date=today,
    time=event_time,
    duration=60,
    location="Toplantı Odası B",
    attendees="Tüm Ekip",
    recurring=False,
    recurrence='none',
    reminders=json.dumps(['15', '5']),
    created_by=user
)

print(f"\n✅ Etkinlik oluşturuldu:")
print(f"   ID: {event.id}")
print(f"   Başlık: {event.title}")
print(f"   Tarih: {event.date}")
print(f"   Saat: {event.time}")

# Bildirimler oluştur
from dashboard.views import create_event_notifications
create_event_notifications(event)

# Oluşturulan bildirimleri göster
notifications = Notification.objects.filter(event=event).order_by('scheduled_time')
print(f"\n✅ {notifications.count()} bildirim oluşturuldu:")
for notif in notifications:
    print(f"   - {notif.title}")
    print(f"     Zaman: {notif.scheduled_time}")
    print(f"     Durum: {notif.status}")

if notifications.count() > 0:
    print("\n🎉 Başarılı! Bildirimler oluşturuldu.")
    print("🔔 Tarayıcıda bildirim ikonuna tıklayın ve bildirimleri görün.")
else:
    print("\n⚠️ Bildirim oluşturulamadı. Lütfen timezone ayarlarını kontrol edin.")
