#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metis_admin.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from dashboard.models import Event, Notification
import json

def create_test_event_and_notifications():
    """Test etkinliği ve bildirimleri oluştur"""
    
    # İlk kullanıcıyı al (veya oluştur)
    try:
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            print(f"Test kullanıcısı oluşturuldu: {user.username}")
    except Exception as e:
        print(f"Kullanıcı hatası: {e}")
        return
    
    # Test etkinliği oluştur (5 dakika sonra)
    event_time = timezone.now() + timedelta(minutes=5)
    
    try:
        event = Event.objects.create(
            title="Test Toplantısı",
            description="Bu bir test toplantısıdır. Bildirim sistemi test ediliyor.",
            type="meeting",
            priority="high",
            date=event_time.date(),
            time=event_time.time(),
            duration=60,
            location="Toplantı Odası A",
            attendees="test@example.com",
            recurring=False,
            recurrence="none",
            reminders=json.dumps(["2", "5"]),  # 2 ve 5 dakika önce hatırlatıcı
            created_by=user
        )
        print(f"Test etkinliği oluşturuldu: {event.title} - {event.date} {event.time}")
        
        # Bildirimler oluştur
        # 5 dakika önce hatırlatıcı
        reminder_5min = event_time - timedelta(minutes=5)
        notification_5min = Notification.objects.create(
            title=f"Etkinlik Hatırlatıcısı: {event.title}",
            message=f"{event.title} etkinliği 5 dakika sonra başlayacak. Konum: {event.location}",
            type='event_reminder',
            event=event,
            user=user,
            scheduled_time=reminder_5min,
            extra_data=json.dumps({
                'event_id': event.id,
                'reminder_minutes': 5,
                'event_type': event.type,
                'event_priority': event.priority
            })
        )
        print(f"5 dakika hatırlatıcısı oluşturuldu: {reminder_5min}")
        
        # 2 dakika önce hatırlatıcı
        reminder_2min = event_time - timedelta(minutes=2)
        notification_2min = Notification.objects.create(
            title=f"Etkinlik Hatırlatıcısı: {event.title}",
            message=f"{event.title} etkinliği 2 dakika sonra başlayacak. Hazır olun!",
            type='event_reminder',
            event=event,
            user=user,
            scheduled_time=reminder_2min,
            extra_data=json.dumps({
                'event_id': event.id,
                'reminder_minutes': 2,
                'event_type': event.type,
                'event_priority': event.priority
            })
        )
        print(f"2 dakika hatırlatıcısı oluşturuldu: {reminder_2min}")
        
        # Etkinlik başlangıç bildirimi
        notification_start = Notification.objects.create(
            title=f"Etkinlik Başlıyor: {event.title}",
            message=f"{event.title} etkinliği şimdi başlıyor! Süre: {event.get_duration_display()}",
            type='event_start',
            event=event,
            user=user,
            scheduled_time=event_time,
            extra_data=json.dumps({
                'event_id': event.id,
                'event_type': event.type,
                'event_priority': event.priority,
                'duration': event.duration
            })
        )
        print(f"Başlangıç bildirimi oluşturuldu: {event_time}")
        
        # Hemen gönderilebilecek bir test bildirimi
        test_notification = Notification.objects.create(
            title="Hoş Geldiniz!",
            message="Bildirim sistemi başarıyla kuruldu ve çalışıyor. Bu bir test bildirimidir.",
            type='info',
            user=user,
            scheduled_time=timezone.now() - timedelta(seconds=1),  # Hemen gönderilsin
            extra_data=json.dumps({
                'test': True,
                'system': 'notification_system'
            })
        )
        print(f"Test bildirimi oluşturuldu: {test_notification.title}")
        
        print("\n=== ÖZET ===")
        print(f"Etkinlik: {event.title}")
        print(f"Tarih/Saat: {event.date} {event.time}")
        print(f"Toplam {Notification.objects.filter(user=user).count()} bildirim oluşturuldu")
        print(f"Kullanıcı: {user.username}")
        print("\nBildirim sistemi test edilmeye hazır!")
        
    except Exception as e:
        print(f"Etkinlik oluşturma hatası: {e}")

if __name__ == "__main__":
    create_test_event_and_notifications()