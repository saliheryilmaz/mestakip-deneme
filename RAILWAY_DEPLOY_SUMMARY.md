# Railway Deployment Hazır! 🚀

## ✅ Yapılan Değişiklikler

### 1. **metis_admin/settings.py** - Railway için optimize edildi
- ✅ SSL redirect devre dışı (Railway otomatik HTTPS sağlar)
- ✅ ALLOWED_HOSTS'a Railway domain'leri eklendi
- ✅ 0.0.0.0 host eklendi
- ✅ Environment variables ile esnek konfigürasyon

### 2. **nixpacks.toml** - Build süreci optimize edildi
- ✅ Python 3.11.0
- ✅ Collectstatic komutu eklendi
- ✅ Start komutu düzenlendi

### 3. **Procfile** - Gunicorn konfigürasyonu eklendi
- ✅ Automatic migration
- ✅ Gunicorn WSGI server

### 4. **railway.json** - Silindi
- ✅ Nixpacks.toml ile çakışma önlendi

### 5. **.gitignore** - Güncellendi
- ✅ staticfiles/ ve db.sqlite3 eklendi
- ✅ dist-modern/ eklendi

## 🚀 Hızlı Başlangıç

### 1. Railway'a Deploy Edin

```bash
# Railway CLI ile (Opsiyonel)
npm i -g @railway/cli
railway login
railway init
railway up
```

VEYA Web UI ile:
1. [railway.app](https://railway.app) → GitHub ile login
2. New Project → Deploy from GitHub repo
3. Reponuzu seçin

### 2. Environment Variables Ekleyin

Railway Dashboard > Settings > Variables:

```
SECRET_KEY=buraya-güvenli-bir-key-oluşturun
DEBUG=False
```

**Güvenli SECRET_KEY oluşturmak için:**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. PostgreSQL Database (Opsiyonel ama Önerilir)

1. Railway Dashboard'da → New → Database → PostgreSQL
2. Railway otomatik olarak DATABASE_URL ekleyecek

### 4. Deploy'i Başlatın

Railway otomatik olarak:
- ✅ Dependencies yükler
- ✅ Collectstatic çalıştırır
- ✅ Migration'ları çalıştırır
- ✅ Gunicorn server'ı başlatır

### 5. Domain Alma

1. Settings → Generate Domain
2. Projeniz `https://your-app.up.railway.app` adresinde çalışacak

### 6. İlk Kullanım

**Superuser oluşturmak için:**
```bash
# Railway Console'dan
python manage.py createsuperuser
```

## 📋 Gerekli Dosyalar

| Dosya | Durum | Açıklama |
|-------|-------|----------|
| Procfile | ✅ Hazır | Gunicorn server config |
| nixpacks.toml | ✅ Hazır | Build config |
| requirements.txt | ✅ Hazır | Dependencies |
| runtime.txt | ✅ Hazır | Python version |
| settings.py | ✅ Hazır | Railway config |
| /health/ endpoint | ✅ Hazır | Healthcheck |
| railway.json | ❌ Silindi | Nixpacks ile çakışma |

## ⚠️ Önemli Notlar

1. **SECRET_KEY**: Mutlaka güvenli bir key kullanın (50+ karakter)
2. **DEBUG**: Production'da False olmalı
3. **Database**: PostgreSQL kullanmanız önerilir (Railway'de ücretsiz)
4. **Static Files**: WhiteNoise ile servis ediliyor
5. **HTTPS**: Railway otomatik sağlar

## 🐛 Sorun Giderme

### Build Hatası
```bash
# Railway console'dan
python manage.py collectstatic --noinput
python manage.py migrate
```

### Database Sorunu
```bash
# PostgreSQL varsa
DATABASE_URL otomatik eklenir
# Yoksa SQLite kullanılır (geçici)
```

### Static Files Yüklenmiyor
- Railway dashboard'dan Variables kontrol edin
- `DEBUG=False` olmalı
- Console'dan collectstatic çalıştırın

## 📚 Detaylı Dokümantasyon

Tüm detaylar için `RAILWAY_DEPLOY.md` dosyasına bakın.

## ✨ Proje Özellikleri

- ✅ Django 5.2.7
- ✅ Gunicorn WSGI Server
- ✅ WhiteNoise Static Files
- ✅ PostgreSQL/SQLite Support
- ✅ Healthcheck Endpoint
- ✅ HTTPS/SSL Support
- ✅ Security Headers
- ✅ Automatic Migrations

## 🎉 Başarılı Deploy İçin Kontrol Listesi

- [ ] Railway'de proje oluşturuldu
- [ ] GitHub repo bağlandı
- [ ] SECRET_KEY environment variable eklendi
- [ ] DEBUG=False environment variable eklendi
- [ ] PostgreSQL database eklendi (opsiyonel)
- [ ] Build başarıyla tamamlandı
- [ ] Domain alındı
- [ ] Uygulama https://your-app.up.railway.app adresinde çalışıyor
- [ ] Healthcheck (/health/) çalışıyor
- [ ] Superuser oluşturuldu

## 💡 İpuçları

1. İlk deploy sonrası Railway'den console açın ve superuser oluşturun
2. `/health/` endpoint'i Railway tarafından otomatik kullanılır
3. Günlükleri takip etmek için Railway Dashboard > Deployments > View Logs
4. Railway ücretsiz planı günde 500 saatlik runtime ve 5$ kadar kredi verir

## 🎯 Sonuç

Projeniz artık Railway'de deploy edilmeye hazır! Yukarıdaki adımları takip ederek 5 dakikada canlıya alabilirsiniz.

Herhangi bir sorun yaşarsanız Railway Dashboard > Deployments > View Logs'dan hata mesajlarını kontrol edin.

