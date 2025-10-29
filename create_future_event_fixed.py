#!/usr/bin/env python
"""Gelecek tarihli test etkinliği ve bildirimleri oluştur (timezone düzeltmeli)"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from dashboard.models import Event, Notification
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
import json

# Kullanıcıyı al (erhan kullanıcısı)
try:
    user = User.objects.get(username='erhan')
except User.DoesNotExist:
    print("❌ 'erhan' kullanıcısı bulunamadı!")
    exit(1)

# Gelecek tarihli etkinlik oluştur (2 saat sonra)
# timezone.now() kullanarak doğru timezone'da oluştur
future_datetime = timezone.now() + timedelta(hours=2)
event_date = future_datetime.date()
event_time = future_datetime.time()

print(f"Şu anki zaman: {timezone.now()}")
print(f"Etkinlik zamanı: {future_datetime}")

# Etkinlik oluştur
event = Event.objects.create(
    title="Önemli Toplantı - Test",
    description="Bu bir test toplantısıdır. Bildirimler 15 ve 5 dakika önce gelecektir.",
    type='meeting',
    priority='high',
    date=event_date,
    time=event_time,
    duration=60,
    location="Toplantı Odası A",
    attendees="Ekip Üyeleri",
    recurring=False,
    recurrence='none',
    reminders=json.dumps(['15', '5']),  # 15 ve 5 dakika önce hatırlatıcılar
    created_by=user
)

print(f"\n✅ Etkinlik oluşturuldu:")
print(f"   Başlık: {event.title}")
print(f"   Tarih: {event.date}")
print(f"   Saat: {event.time}")
print(f"   Kullanıcı: {event.created_by.username}")

# Bildirimler oluştur
from dashboard.views import create_event_notifications
create_event_notifications(event)

# Oluşturulan bildirimleri göster
notifications = Notification.objects.filter(event=event).order_by('scheduled_time')
print(f"\n✅ {notifications.count()} bildirim oluşturuldu:")
for notif in notifications:
    time_diff = notif.scheduled_time - timezone.now()
    minutes_until = int(time_diff.total_seconds() / 60)
    print(f"   - {notif.title}")
    print(f"     Zaman: {notif.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"     Durum: {notif.status}")
    print(f"     {minutes_until} dakika sonra")

print("\n🎉 Test etkinliği ve bildirimleri başarıyla oluşturuldu!")
print("📅 Takvim sayfasına gidin ve etkinliği görün.")
print("🔔 Bildirimler zamanı geldiğinde otomatik olarak görünecektir.")
