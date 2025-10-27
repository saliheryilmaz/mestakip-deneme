# DATABASE_URL Sorunu - Çözüm

## ❌ Sorun:
```
DATABASE_URL parsing error: Port could not be cast to integer value as 'port'
```

Bu, DATABASE_URL'in formatının yanlış olduğu anlamına geliyor.

## ✅ Çözüm - Railway Dashboard'da:

### 1. Railway Dashboard'a Git
https://railway.app → Projeniz

### 2. Settings > Variables

### 3. DATABASE_URL'i Sil ve Yeniden Oluştur

**Seçenek A - PostgreSQL'i Sil ve Yeniden Ekle:**
1. PostgreSQL database'i sil
2. **NEW** → **Database** → **PostgreSQL** → **Add PostgreSQL**
3. Railway otomatik olarak doğru format ile DATABASE_URL ekleyecek

**Seçenek B - DATABASE_URL'i Manuel Düzelt:**

Eğer DATABASE_URL şu formatta ise (YANLIŞ):
```
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

Şöyle olmalı (DOĞRU):
```
DATABASE_URL=postgresql://postgres:şifre@hostname.railway.internal:5432/railway
```

AMA: **Bu formatı manuel yapmana gerek yok!**
Railway PostgreSQL ekleyince otomatik doğru format ekler.

## 🎯 EN KOLAY ÇÖZÜM:

1. Railway Dashboard
2. PostgreSQL database'i **SİL**
3. **NEW** → **Database** → **PostgreSQL** → **Add**
4. Railway otomatik doğru DATABASE_URL ekleyecek ✅

## 📋 Kontrol Listesi:

Railway Dashboard'da şunlar olmalı:

✅ **SECRET_KEY** = `$6j$h5_p1mlz6zen_+2g^+c^ahak=(5$)lvks7t(un)h^cn+a7`

✅ **DEBUG** = `False`

✅ **DATABASE_URL** = Railway PostgreSQL tarafından otomatik oluşturulacak

✅ **PostgreSQL Database** = Bir PostgreSQL database var

## ⚠️ ÖNEMLİ:

DATABASE_URL'i manuel yazmana gerek yok! 
Railway PostgreSQL eklediğinde otomatik oluşturuyor.

Eğer manuel eklediysen, SİL ve PostgreSQL'i yeniden ekle.

