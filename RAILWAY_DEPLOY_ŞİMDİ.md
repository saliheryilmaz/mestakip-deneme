# 🚀 Railway Deploy - ŞİMDİ YAPILACAKLAR

## ✅ 1. Railway Dashboard'a Git

[Railway Dashboard'a Git →](https://railway.app)

## 🔑 2. Environment Variables Ekle

Settings > Variables kısmından şu değişkenleri ekle:

### SECRET_KEY (GEREKLİ!)
Variable Name: `SECRET_KEY`
Value: `lgqz)au$7n^5_u#_-+x4id-j9@!8)=h&3!ao6&+b#j4=pvp0r!`

### DEBUG (GEREKLİ!)
Variable Name: `DEBUG`
Value: `False`

**Ekle Butonuna Tıkla!**

## 🗄️ 3. PostgreSQL Database Ekle (ÇOK ÖNEMLİ!)

1. Railway Dashboard'da projenizin yanında **"New"** butonuna tıkla
2. **"Database"** seç
3. **"Add PostgreSQL"** butonuna tıkla
4. Railway otomatik olarak `DATABASE_URL` ekleyecek ✅

Bu olmadan uygulama çalışmaz!

## ⚡ 4. Deploy Otomatik Başlayacak!

Railway GitHub'ı izliyor, otomatik olarak yeni kodu alacak ve deploy başlatacak.

## 📊 5. Logları İzle

Railway Dashboard > Deployments > "View Logs"

Şunları görmelisin:
```
🚂 Railway environment detected!
📊 DATABASE_URL: Set
🔑 SECRET_KEY: Set
🐛 DEBUG: False
✅ PostgreSQL configuration looks good!
🚀 Starting Gunicorn on PORT: 8000
```

## ✅ 6. Test Et

Deploy tamamlandıktan sonra:

1. Settings > Domains > "Generate Domain" butonuna tıkla
2. Domain'e git (örn: `https://your-app.up.railway.app`)
3. `/health/` ekle → 200 OK dönmeli
4. Ana sayfaya git

## 👤 7. İlk Kullanım - Superuser Oluştur

Railway Dashboard > Service > "Open Console" butonuna tıkla:

```bash
python manage.py createsuperuser
```

Kullanıcı adı, email ve şifre gir.

## ✨ Tamamlandı!

Uygulaman artık Railway'de çalışıyor! 🎉

---

## 🐛 Sorun Çıkarsa

### Eğer hala "Application failed to respond" görüyorsan:

1. Railway Dashboard > Deployments > View Logs
2. Hata mesajını oku
3. Genellikle:
   - DATABASE_URL eksik → PostgreSQL ekle
   - SECRET_KEY eksik → Environment variable ekle
   - Build hatası → Logları kontrol et

### Console'dan Manuel Kontrol

Railway > Service > "Open Console":

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

**Önemli:** Bu 3 adımı yap (1. SECRET_KEY, 2. DEBUG, 3. PostgreSQL), gerisi otomatik olacak!

