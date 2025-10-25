# Güvenli Deployment Talimatları

Bu dosya, Django projesinin güvenli bir şekilde deploy edilmesi için gerekli adımları içerir.

## 🔒 Güvenlik Ayarları

### 1. Environment Variables (Railway)
Railway dashboard'da aşağıdaki environment variables'ları ayarlayın:

```bash
DEBUG=False
SECRET_KEY=your-super-secret-key-here
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### 2. Güvenlik Özellikleri

#### HTTPS Zorlaması
- Tüm HTTP trafiği otomatik olarak HTTPS'e yönlendirilir
- HSTS (HTTP Strict Transport Security) etkin
- Güvenli cookie ayarları

#### Güvenlik Headers
- Content Security Policy (CSP)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

#### Cookie Güvenliği
- Session cookies sadece HTTPS üzerinden gönderilir
- CSRF cookies güvenli modda
- SameSite=Strict ayarları

## 🚀 Deployment Adımları

### Railway'de Deploy Etme

1. **Railway Dashboard'a giriş yapın**
2. **Yeni proje oluşturun**
3. **GitHub repository'nizi bağlayın**
4. **Environment variables'ları ayarlayın** (yukarıdaki liste)
5. **Deploy butonuna tıklayın**

### Manuel Deploy

```bash
# 1. Gerekli paketleri yükleyin
pip install -r requirements.txt

# 2. Static dosyaları toplayın
python manage.py collectstatic --noinput

# 3. Veritabanı migration'larını çalıştırın
python manage.py migrate

# 4. Production sunucusunu başlatın
gunicorn metis_admin.wsgi:application --bind 0.0.0.0:$PORT
```

## 🔍 Güvenlik Testi

### SSL Test
- [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/) kullanarak SSL yapılandırmanızı test edin
- A+ notu almanız hedeflenir

### Güvenlik Headers Test
- [Security Headers](https://securityheaders.com/) ile güvenlik header'larınızı test edin
- A+ notu almanız hedeflenir

### Manuel Test
```bash
# HTTPS yönlendirmesini test edin
curl -I http://your-domain.com
# 301 veya 302 redirect almalısınız

# HTTPS bağlantısını test edin
curl -I https://your-domain.com
# 200 OK almalısınız
```

## ⚠️ Önemli Notlar

1. **SECRET_KEY**: Production'da mutlaka güçlü bir secret key kullanın
2. **DEBUG**: Production'da DEBUG=False olmalı
3. **ALLOWED_HOSTS**: Sadece gerekli domain'leri ekleyin
4. **Database**: Production'da PostgreSQL kullanın (SQLite değil)

## 🛠️ Sorun Giderme

### HTTPS Çalışmıyor
- Railway'de environment variables'ları kontrol edin
- SECURE_SSL_REDIRECT=True olduğundan emin olun
- SECURE_PROXY_SSL_HEADER ayarını kontrol edin

### Static Files Yüklenmiyor
- WhiteNoise ayarlarını kontrol edin
- collectstatic komutunu çalıştırın
- STATIC_ROOT ayarını kontrol edin

### CSRF Hatası
- CSRF_COOKIE_SECURE=True olduğundan emin olun
- HTTPS bağlantısı kullandığınızdan emin olun
