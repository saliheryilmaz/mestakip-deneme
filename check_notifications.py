#!/usr/bin/env python
"""Bildirim durumlarını kontrol et"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from dashboard.models import Notification, Event
from django.utils import timezone

print("=" * 60)
print("BİLDİRİM DURUMU RAPORU")
print("=" * 60)

# Tüm bildirimleri getir
notifications = Notification.objects.all().order_by('-scheduled_time')

print(f"\nToplam Bildirim Sayısı: {notifications.count()}")
print(f"Toplam Etkinlik Sayısı: {Event.objects.count()}")

# Durum bazında sayılar
pending_count = Notification.objects.filter(status='pending').count()
sent_count = Notification.objects.filter(status='sent').count()
read_count = Notification.objects.filter(status='read').count()
dismissed_count = Notification.objects.filter(status='dismissed').count()

print(f"\nDurum Bazında:")
print(f"  - Bekliyor (pending): {pending_count}")
print(f"  - Gönderildi (sent): {sent_count}")
print(f"  - Okundu (read): {read_count}")
print(f"  - Kapatıldı (dismissed): {dismissed_count}")

# Kullanıcı bazında
from django.contrib.auth.models import User
users = User.objects.all()
print(f"\nKullanıcı Bazında:")
for user in users:
    user_nots = Notification.objects.filter(user=user)
    unread = user_nots.filter(status__in=['pending', 'sent']).count()
    print(f"  - {user.username}: {user_nots.count()} bildirim ({unread} okunmamış)")

# Son 10 bildirimi detaylı göster
print(f"\n{'=' * 60}")
print("SON 10 BİLDİRİM:")
print(f"{'=' * 60}")

for notification in notifications[:10]:
    now = timezone.now()
    time_diff = notification.scheduled_time - now
    time_status = "GEÇMİŞ" if time_diff.total_seconds() < 0 else f"{int(time_diff.total_seconds() / 60)} dk sonra"
    
    print(f"\nID: {notification.id}")
    print(f"  Başlık: {notification.title}")
    print(f"  Mesaj: {notification.message[:50]}...")
    print(f"  Durum: {notification.status}")
    print(f"  Tür: {notification.type}")
    print(f"  Kullanıcı: {notification.user.username}")
    print(f"  Planlanmış Zaman: {notification.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Zaman Durumu: {time_status}")
    if notification.event:
        print(f"  İlişkili Etkinlik: {notification.event.title}")

print(f"\n{'=' * 60}")
