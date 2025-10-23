# Metis Bootstrap Admin Template - Django Version

Bu proje, orijinal Bootstrap Admin Template'inin Django versiyonudur. Modern, responsive ve kullanıcı dostu bir admin paneli sağlar.

## Özellikler

- ✅ Django 5.2.7 ile uyumlu
- ✅ Bootstrap 5.3.7 ile modern tasarım
- ✅ Responsive tasarım (mobil uyumlu)
- ✅ Dark/Light tema desteği
- ✅ Modern JavaScript (ES6+)
- ✅ Chart.js entegrasyonu
- ✅ Alpine.js ile reaktif bileşenler
- ✅ Bootstrap Icons
- ✅ PWA desteği

## Kurulum

### 1. Sanal Ortam Oluşturma

```bash
python -m venv venv
```

### 2. Sanal Ortamı Aktifleştirme

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleme

```bash
pip install -r requirements.txt
```

### 4. Veritabanı Migrasyonları

```bash
python manage.py migrate
```

### 5. Sunucuyu Başlatma

```bash
python manage.py runserver
```

Tarayıcınızda `http://127.0.0.1:8000` adresine giderek uygulamayı görüntüleyebilirsiniz.

## Proje Yapısı

```
metis_admin/
├── templates/
│   ├── base.html              # Ana template
│   └── dashboard/
│       ├── index.html         # Dashboard ana sayfası
│       ├── analytics.html     # Analytics sayfası
│       ├── users.html         # Kullanıcılar sayfası
│       ├── products.html      # Ürünler sayfası
│       ├── orders.html        # Siparişler sayfası
│       ├── forms.html         # Formlar sayfası
│       ├── elements.html      # UI Elementleri
│       ├── reports.html       # Raporlar sayfası
│       ├── messages.html      # Mesajlar sayfası
│       ├── calendar.html      # Takvim sayfası
│       ├── files.html         # Dosyalar sayfası
│       ├── settings.html      # Ayarlar sayfası
│       ├── security.html      # Güvenlik sayfası
│       └── help.html          # Yardım sayfası
├── static/                    # Static dosyalar (CSS, JS, Images)
├── dashboard/                 # Dashboard uygulaması
│   ├── views.py              # View fonksiyonları
│   ├── urls.py               # URL yapılandırması
│   └── models.py             # Veritabanı modelleri
├── metis_admin/              # Ana Django projesi
│   ├── settings.py           # Django ayarları
│   ├── urls.py               # Ana URL yapılandırması
│   └── wsgi.py               # WSGI yapılandırması
└── manage.py                 # Django yönetim scripti
```

## Kullanım

### Dashboard
Ana sayfa olan dashboard'da genel istatistikler, grafikler ve son aktiviteler görüntülenir.

### Navigasyon
Sol sidebar'dan tüm sayfalara erişebilirsiniz:
- **Dashboard**: Ana sayfa
- **Analytics**: Analitik veriler
- **Users**: Kullanıcı yönetimi
- **Products**: Ürün yönetimi
- **Orders**: Sipariş yönetimi
- **Forms**: Form yönetimi
- **Elements**: UI bileşenleri
- **Reports**: Raporlar
- **Messages**: Mesajlar
- **Calendar**: Takvim
- **Files**: Dosya yönetimi
- **Settings**: Ayarlar
- **Security**: Güvenlik
- **Help**: Yardım

### Tema Değiştirme
Sağ üst köşedeki tema butonuna tıklayarak dark/light tema arasında geçiş yapabilirsiniz.

### Responsive Tasarım
Uygulama tüm cihazlarda (masaüstü, tablet, mobil) mükemmel çalışır.

## Geliştirme

### Yeni Sayfa Ekleme

1. `templates/dashboard/` klasörüne yeni template dosyası ekleyin
2. `dashboard/views.py` dosyasına view fonksiyonu ekleyin
3. `dashboard/urls.py` dosyasına URL pattern ekleyin

### Static Dosya Ekleme

Static dosyaları `static/` klasörüne ekleyin ve template'lerde şu şekilde kullanın:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## İletişim

Herhangi bir sorunuz veya öneriniz için issue açabilirsiniz.
