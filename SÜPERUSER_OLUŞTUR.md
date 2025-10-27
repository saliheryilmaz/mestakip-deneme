# 👤 Railway'de Superuser Oluşturma

## ❌ Sorun:
Giriş yaparken "Kullanıcı adı veya şifre hatalı!" hatası alıyorsun.

**Sebep:** Railway'de yeni PostgreSQL database var ama henüz kullanıcı oluşturulmamış.

## ✅ ÇÖZÜM - 3 DAKİKA:

### Railway Console'dan Superuser Oluştur:

1. **Railway Dashboard'a Git:**
   - https://railway.app
   - Projenizi açın

2. **Console Aç:**
   - Proje dashboard'ında **"Open Console"** veya **"Shell"** butonuna tıkla
   - Ya da **Service** > **Console** > **Open Console**

3. **Superuser Oluştur:**
   Console'da şu komutu çalıştır:
   ```bash
   python manage.py createsuperuser
   ```

4. **Bilgileri Gir:**
   - Username (kullanıcı adı): İstediğin kullanıcı adı (örn: admin)
   - Email: Email adresin (örn: admin@example.com)
   - Password: Güvenli bir şifre
   - Password (again): Şifreyi tekrar gir

Örnek:
```
Username: admin
Email address: admin@example.com  
Password: ********
Password (again): ********
```

5. **Login Yap:**
   - Railway domain'ine git (örn: https://your-app.up.railway.app)
   - Oluşturduğun kullanıcı adı ve şifre ile giriş yap

---

## 🎯 Alternatif: Manuel User Oluştur

Eğer `createsuperuser` çalışmazsa:

```bash
python manage.py shell
```

Sonra shell'de:
```python
from django.contrib.auth.models import User

# Yeni kullanıcı oluştur
user = User.objects.create_user('admin', 'admin@example.com', 'yourpassword')
user.is_staff = True
user.is_superuser = True
user.save()

print("Kullanıcı oluşturuldu!")
exit()
```

---

## 🔍 Kontrol:

Kullanıcı var mı kontrol et:
```bash
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.count(), 'kullanıcı var')"
```

---

## 💡 İpucu:

Railway'de her yeni deploy veya database değişikliğinden sonra superuser oluşturman gerekebilir.

Artık giriş yapabilmelisin! 🎉

