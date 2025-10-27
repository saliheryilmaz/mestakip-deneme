# Railway Deployment Rehberi

Bu proje Railway'de deploy edilmeye hazırdır. Aşağıdaki adımları takip edin.

## Railway'de Deploy Etme Adımları

### 1. Railway'a Giriş Yapın
- [Railway.app](https://railway.app) adresine gidin
- GitHub hesabınızla giriş yapın

### 2. Yeni Proje Oluşturun
- "New Project" butonuna tıklayın
- "Deploy from GitHub repo" seçeneğini seçin
- Reponuzu seçin ve import edin

### 3. Environment Variables Ekleyin

Railway dashboard'da Settings > Variables bölümünden aşağıdaki environment variables'ı ekleyin:

```
SECRET_KEY=django-insecure-buraya-guvenli-bir-secret-key-yazin-unique-olmalı
DEBUG=False
DJANGO_SETTINGS_MODULE=metis_admin.settings
```

**Önemli:** SECRET_KEY için güvenli bir key oluşturun:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 4. PostgreSQL Database Ekleyin (Opsiyonel ama Önerilir)
- Railway dashboard'da "New" > "Database" > "PostgreSQL" seçin
- Database otomatik olarak `DATABASE_URL` environment variable olarak eklenecek
- Proje PostgreSQL'i otomatik kullanacak

### 5. Deploy'i Başlatın
- Railway otomatik olarak deploy başlatacak
- "Deploy Logs" sekmesinde build sürecini takip edebilirsiniz

### 6. Domain Ekleme
- Deploy tamamlandıktan sonra "Settings" > "Generate Domain" butonuna tıklayın
- Size özel bir `up.railway.app` domain'i verilecek

## Build Süreci

Proje aşağıdaki aşamalardan geçecek:

1. **Setup**: Python 3.11 ve pip kurulumu
2. **Install**: requirements.txt'deki paketlerin kurulumu
3. **Build**: Static dosyaların toplanması (`collectstatic`)
4. **Start**: 
   - Database migration'ları çalıştırılır
   - Gunicorn server başlatılır

## Healthcheck

Proje `/health/` endpoint'i ile healthcheck'i destekler. Railway otomatik olarak bu endpoint'i kullanır.

## Gerekli Dosyalar

- ✅ `Procfile`: Gunicorn başlatma komutu
- ✅ `nixpacks.toml`: Build süreci konfigürasyonu
- ✅ `requirements.txt`: Python dependencies
- ✅ `runtime.txt`: Python versiyonu
- ✅ `metis_admin/settings.py`: Railway uyumlu ayarlar
- ✅ `/health/` endpoint: Healthcheck

## Sorun Giderme

### Static Files Sorunu
Eğer CSS/JS dosyaları yüklenmiyorsa:
- Railway console'dan şu komutu çalıştırın:
```bash
python manage.py collectstatic --noinput
```

### Database Migration Sorunu
```bash
python manage.py migrate --noinput
```

### Build Hatası
- Railway Dashboard > Deployments > View Logs'dan hata detaylarını kontrol edin
- Genellikle dependency veya Python versiyonu sorunları olabilir

## İlk Kullanım

1. Deploy tamamlandıktan sonra domain'inize gidin
2. Admin paneli için: `https://your-domain.up.railway.app/admin/`
3. Superuser oluşturmak için Railway Console'dan:
```bash
python manage.py createsuperuser
```

## Güvenlik

- ✅ SECRET_KEY environment variable ile yönetiliyor
- ✅ DEBUG=False production'da
- ✅ SECURE SSL cookies ve headers aktif
- ✅ Allowed hosts yapılandırıldı
- ✅ WhiteNoise ile static file serving
- ✅ Railway PostgreSQL varsa kullanılır, yoksa SQLite

## Desteklenen Özellikler

- ✅ Django 5.2.7
- ✅ PostgreSQL/SQLite database
- ✅ Gunicorn WSGI server
- ✅ WhiteNoise static files
- ✅ Healthcheck endpoint
- ✅ HTTPS/SSL support

