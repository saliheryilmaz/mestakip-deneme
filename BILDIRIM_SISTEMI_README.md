# 📅 Takvim Bildirim Sistemi

Bu sistem, takvim etkinlikleri için otomatik bildirim gönderme özelliği sağlar. Kullanıcılar etkinlik oluştururken hatırlatıcı zamanları belirleyebilir ve sistem bu hatırlatıcıları otomatik olarak gönderir.

## 🚀 Özellikler

### ✅ Tamamlanan Özellikler

1. **Etkinlik Oluşturma**
   - Takvim sayfasında etkinlik oluşturma
   - Çoklu hatırlatıcı seçimi (5dk, 15dk, 30dk, 1 saat, 1 gün önce)
   - Etkinlik türleri: Etkinlik, Toplantı, Görev, Hatırlatıcı, Son Tarih
   - Öncelik seviyeleri: Düşük, Orta, Yüksek

2. **Bildirim Sistemi**
   - Otomatik bildirim oluşturma
   - Zamanı gelen bildirimleri gönderme
   - Bildirim durumu takibi (Bekliyor, Gönderildi, Okundu, Kapatıldı)
   - Navbar'da bildirim dropdown'ı
   - Okunmamış bildirim sayacı

3. **Bildirim Türleri**
   - Etkinlik hatırlatıcıları
   - Etkinlik başlangıç bildirimleri
   - Sistem bildirimleri
   - Bilgi, uyarı ve hata bildirimleri

4. **Yönetim Paneli**
   - Django admin'de bildirim yönetimi
   - Toplu işlemler (okundu işaretle, gönderildi işaretle)
   - Bildirim filtreleme ve arama

## 📋 Kurulum ve Kullanım

### 1. Veritabanı Güncellemesi
```bash
python manage.py makemigrations dashboard
python manage.py migrate
```

### 2. Test Verisi Oluşturma
```bash
python test_notifications.py
```

### 3. Bildirim Gönderme (Manuel)
```bash
# Sadece kontrol et
python manage.py send_notifications --dry-run

# Gerçekten gönder
python manage.py send_notifications
```

### 4. Otomatik Bildirim Gönderme (Cron Job)
```bash
# Her dakika kontrol et
* * * * * cd /path/to/project && python manage.py send_notifications

# Her 5 dakikada bir kontrol et
*/5 * * * * cd /path/to/project && python manage.py send_notifications
```

## 🎯 Kullanım Senaryoları

### Etkinlik Oluşturma
1. Dashboard'da "Takvim" sayfasına git
2. "Etkinlik Ekle" butonuna tıkla
3. Etkinlik bilgilerini doldur
4. Hatırlatıcı zamanlarını seç (Ctrl+Click ile çoklu seçim)
5. "Etkinlik Oluştur" butonuna tıkla

### Bildirimleri Görüntüleme
1. Navbar'daki zil ikonuna tıkla
2. Bildirim listesini görüntüle
3. "Okundu İşaretle" veya "Kapat" butonlarını kullan
4. "Tümünü Okundu İşaretle" ile toplu işlem yap

## 🔧 API Endpoints

### Bildirim API'leri
- `GET /dashboard/api/notifications/` - Bildirimleri listele
- `POST /dashboard/api/notifications/{id}/read/` - Bildirimi okundu işaretle
- `POST /dashboard/api/notifications/read-all/` - Tümünü okundu işaretle
- `POST /dashboard/api/notifications/{id}/dismiss/` - Bildirimi kapat

### Etkinlik API'leri
- `GET /dashboard/api/events/` - Etkinlikleri listele
- `POST /dashboard/api/events/create/` - Etkinlik oluştur

## 📊 Veritabanı Modelleri

### Event (Etkinlik)
- Başlık, açıklama, tür, öncelik
- Tarih, saat, süre
- Konum, katılımcılar
- Tekrarlama ayarları
- Hatırlatıcı zamanları (JSON)

### Notification (Bildirim)
- Başlık, mesaj, tür, durum
- İlişkili etkinlik (opsiyonel)
- Hedef kullanıcı
- Planlanmış zaman, gönderilme zamanı, okunma zamanı
- Ek veriler (JSON)

## 🎨 Frontend Özellikleri

### JavaScript Bildirim Sistemi
- Otomatik bildirim yenileme (30 saniye)
- Gerçek zamanlı bildirim sayacı
- Tarayıcı bildirimi desteği
- SweetAlert2 entegrasyonu

### CSS Stilleri
- Responsive bildirim dropdown'ı
- Dark theme desteği
- Okunmamış bildirim vurgusu
- Bildirim türü ikonları ve renkleri

## 🔄 Otomatik İşlemler

### Bildirim Oluşturma
Etkinlik oluşturulduğunda otomatik olarak:
1. Seçilen hatırlatıcı zamanları için bildirimler oluşturulur
2. Etkinlik başlangıç bildirimi oluşturulur
3. Geçmiş tarihli hatırlatıcılar atlanır

### Bildirim Gönderme
Management command ile:
1. Zamanı gelen bekleyen bildirimler bulunur
2. Bildirimler "gönderildi" olarak işaretlenir
3. Hata durumunda log kaydı tutulur

## 🛠️ Geliştirme Notları

### Yeni Bildirim Türü Ekleme
1. `Notification.TYPE_CHOICES`'a yeni tür ekle
2. `get_type_icon()` ve `get_type_color()` metodlarını güncelle
3. Frontend'de ikon ve renk tanımlarını ekle

### Yeni Hatırlatıcı Zamanı Ekleme
1. `addEventModal` component'inde `reminderOptions`'a ekle
2. Frontend'de seçenek olarak görünecek

### Email/SMS Entegrasyonu
`send_notifications.py` command'inde bildirim gönderme kısmını genişlet:
```python
# Email gönderme
send_mail(
    subject=notification.title,
    message=notification.message,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[notification.user.email]
)

# SMS gönderme (Twilio, etc.)
# SMS API entegrasyonu
```

## 📱 Mobil Uyumluluk

- Responsive bildirim dropdown'ı
- Touch-friendly butonlar
- Mobil tarayıcı bildirim desteği

## 🔒 Güvenlik

- CSRF koruması
- Kullanıcı bazlı bildirim erişimi
- XSS koruması (HTML escape)
- SQL injection koruması (Django ORM)

## 📈 Performans

- Veritabanı indeksleri
- Sayfalama desteği
- Lazy loading
- Önbellek desteği (gelecekte eklenebilir)

## 🐛 Bilinen Sorunlar

- Tarayıcı bildirimi izni manuel olarak verilmeli
- Çok fazla bildirim performansı etkileyebilir
- Timezone desteği geliştirilmeli

## 🚀 Gelecek Özellikler

- [ ] Email bildirim entegrasyonu
- [ ] SMS bildirim entegrasyonu
- [ ] Push notification desteği
- [ ] Bildirim şablonları
- [ ] Toplu bildirim gönderme
- [ ] Bildirim istatistikleri
- [ ] Kullanıcı bildirim tercihleri
- [ ] Bildirim geçmişi arşivleme

## 📞 Destek

Herhangi bir sorun veya öneriniz için:
- GitHub Issues kullanın
- Dokümantasyonu kontrol edin
- Admin panelinden bildirim loglarını inceleyin

---

**Not:** Bu sistem production ortamında kullanılmadan önce kapsamlı test edilmelidir. Özellikle cron job ayarları ve email/SMS entegrasyonları dikkatli yapılmalıdır.