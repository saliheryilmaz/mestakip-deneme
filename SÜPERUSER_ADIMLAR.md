# 🖥️ Railway Console Nasıl Açılır?

## 📍 Adım Adım Console Açma:

### 1️⃣ Railway Dashboard'a Git
→ https://railway.app

### 2️⃣ Sol Tarafta Projeni Seç
Proje adını göreceksin (örn: mestakip-2), tıkla

### 3️⃣ "Web Service" Kartını Göreceksin
Ekranda bir kart olacak, üzerine tıkla

### 4️⃣ Üst Bar'da "Console" veya "Shell" Butonunu Bul
Sağ tarafta veya üstte bir buton olacak:
- "Shell" 
- "Console"
- Veya bir terminal ikonu

### 5️⃣ Tıkla - Terminal Açılacak

### 6️⃣ Şu Komutu Çalıştır:
```bash
python manage.py createsuperuser
```

Enter'a bas ve bilgileri gir:
- Username: admin
- Email: admin@example.com  
- Password: şifren
- Password (again): şifren

---

## 🖼️ Görsel Yol:

```
Railway Dashboard
  └── Projen (mestakip-2)
      └── Web Service
          └── ✅ Console/Shell Butonuna Tıkla
              └── Terminal Açılır
                  └── python manage.py createsuperuser
```

---

## 🔍 Alternatif Yerler:

**Eğer Console butonu göremiyorsan:**
1. **Settings** sekmesine git → **Console** 
2. **Deployments** → Son deployment → **View Logs** → **Open Console**
3. Üst menüde **"..."** → **"Open Terminal"**

---

## ✅ Kontrol:

Console açıldı mı? Şunu görmelisin:
```bash
/app $
```

Harika! Artık komut çalıştırabilirsin.

