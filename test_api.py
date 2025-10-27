#!/usr/bin/env python
import requests
import json

# Test API endpoints
base_url = "http://127.0.0.1:8000"

def test_notifications_api():
    """Bildirim API'sini test et"""
    
    # Session oluştur
    session = requests.Session()
    
    # Login sayfasından CSRF token al
    login_url = f"{base_url}/dashboard/login/"
    response = session.get(login_url)
    
    if response.status_code != 200:
        print(f"Login sayfası erişim hatası: {response.status_code}")
        return
    
    # CSRF token'ı bul
    csrf_token = None
    for line in response.text.split('\n'):
        if 'csrfmiddlewaretoken' in line:
            start = line.find('value="') + 7
            end = line.find('"', start)
            csrf_token = line[start:end]
            break
    
    if not csrf_token:
        print("CSRF token bulunamadı")
        return
    
    # Login ol
    login_data = {
        'username': 'admin',
        'password': 'admin',  # Varsayılan şifre
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(login_url, data=login_data)
    
    if response.status_code == 200 and 'dashboard' in response.url:
        print("✓ Giriş başarılı")
    else:
        print(f"✗ Giriş başarısız: {response.status_code}")
        return
    
    # Bildirimler API'sini test et
    notifications_url = f"{base_url}/dashboard/api/notifications/"
    print(f"Testing URL: {notifications_url}")
    response = session.get(notifications_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            notifications = data.get('notifications', [])
            unread_count = data.get('unread_count', 0)
            
            print(f"✓ Bildirimler API çalışıyor")
            print(f"  - Toplam bildirim: {len(notifications)}")
            print(f"  - Okunmamış: {unread_count}")
            
            for notification in notifications[:3]:  # İlk 3 bildirimi göster
                print(f"  - {notification['title']} ({notification['status']})")
        else:
            print(f"✗ API hatası: {data.get('error')}")
    else:
        print(f"✗ API erişim hatası: {response.status_code}")
    
    # Etkinlikler API'sini test et
    events_url = f"{base_url}/dashboard/api/events/"
    response = session.get(events_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            events = data.get('events', [])
            print(f"✓ Etkinlikler API çalışıyor")
            print(f"  - Toplam etkinlik: {len(events)}")
            
            for event in events[:2]:  # İlk 2 etkinliği göster
                print(f"  - {event['title']} ({event['date']} {event['time']})")
        else:
            print(f"✗ Etkinlikler API hatası: {data.get('error')}")
    else:
        print(f"✗ Etkinlikler API erişim hatası: {response.status_code}")

if __name__ == "__main__":
    print("🧪 API Test Başlıyor...")
    test_notifications_api()
    print("✅ Test tamamlandı!")