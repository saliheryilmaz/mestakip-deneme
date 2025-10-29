# Dropdown Butonları Düzeltme

## Sorun
Hem bildirim simgesine (zil ikonu) hem de kullanıcı menüsüne (erhan Eryılmaz) tıklandığında dropdown menüleri açılmıyordu.

## Yapılan Değişiklikler

### 1. HTML Düzeltmeleri (templates/base.html)

#### Bildirim Butonu
```html
<!-- ÖNCE -->
<button class="btn btn-outline-secondary position-relative" type="button"
    data-bs-toggle="dropdown" 
    aria-expanded="false" 
    id="notificationButton">

<!-- SONRA -->
<button class="btn btn-outline-secondary position-relative" type="button"
    data-bs-toggle="dropdown" 
    data-bs-auto-close="outside"
    aria-expanded="false" 
    id="notificationButton">
```

**Değişiklik:** `data-bs-auto-close="outside"` eklendi. Bu, dropdown içindeki butonlara (örn. "Tümünü Okundu İşaretle") tıklandığında dropdown'ın kapanmamasını sağlar.

#### Dropdown Menüsü
```html
<!-- ÖNCE -->
<ul class="dropdown-menu dropdown-menu-end" id="notificationDropdownMenu"
    style="width: 350px; max-height: 400px; overflow-y: auto;">

<!-- SONRA -->
<ul class="dropdown-menu dropdown-menu-end" id="notificationDropdownMenu"
    aria-labelledby="notificationButton"
    style="width: 350px; max-height: 400px; overflow-y: auto;">
```

**Değişiklik:** `aria-labelledby="notificationButton"` eklendi. Bu, erişilebilirlik için gerekli ve dropdown'ın hangi butona bağlı olduğunu belirtir.

#### Kullanıcı Menüsü Butonu
```html
<!-- ÖNCE -->
<button class="btn btn-outline-secondary d-flex align-items-center" type="button"
    data-bs-toggle="dropdown" aria-expanded="false">

<!-- SONRA -->
<button class="btn btn-outline-secondary d-flex align-items-center" type="button"
    data-bs-toggle="dropdown" 
    data-bs-auto-close="true"
    aria-expanded="false"
    id="userMenuButton">
```

**Değişiklikler:**
- `id="userMenuButton"` eklendi
- `data-bs-auto-close="true"` eklendi (menü öğelerine tıklandığında dropdown kapanır)

#### Kullanıcı Menüsü Dropdown
```html
<!-- ÖNCE -->
<ul class="dropdown-menu dropdown-menu-end">

<!-- SONRA -->
<ul class="dropdown-menu dropdown-menu-end" 
    id="userMenuDropdown"
    aria-labelledby="userMenuButton">
```

**Değişiklikler:**
- `id="userMenuDropdown"` eklendi
- `aria-labelledby="userMenuButton"` eklendi

### 2. JavaScript Düzeltmeleri

#### setupEventListeners() Fonksiyonu
```javascript
setupEventListeners() {
    // Tümünü okundu işaretle butonu
    const markAllReadBtn = document.getElementById('markAllReadBtn');
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.markAllAsRead();
        });
    }

    // Bildirim dropdown açıldığında
    const notificationButton = document.getElementById('notificationButton');
    const notificationDropdown = document.getElementById('notificationDropdownMenu');
    
    if (notificationButton && notificationDropdown) {
        // Dropdown açıldığında bildirimleri yükle
        notificationButton.addEventListener('shown.bs.dropdown', () => {
            console.log('Dropdown açıldı, bildirimler yükleniyor...');
            this.loadNotifications();
        });
        
        // İlk yüklemede de bildirimleri getir
        notificationButton.addEventListener('click', (e) => {
            console.log('Bildirim butonu tıklandı');
            // Dropdown'ı manuel olarak aç/kapat
            const dropdown = bootstrap.Dropdown.getInstance(notificationButton);
            if (dropdown) {
                console.log('Dropdown instance bulundu');
            } else {
                console.log('Dropdown instance oluşturuluyor...');
                const newDropdown = new bootstrap.Dropdown(notificationButton);
            }
        });
    }
}
```

**Değişiklikler:**
- Hem `notificationButton` hem de `notificationDropdown` kontrolü eklendi
- Click event listener'ında dropdown instance kontrolü eklendi
- Daha detaylı console log'ları eklendi

#### DOMContentLoaded Event Listener
```javascript
document.addEventListener('DOMContentLoaded', function () {
    console.log('=== Bildirim Sistemi Başlatılıyor ===');
    
    // Bootstrap kontrolü
    if (typeof bootstrap === 'undefined') {
        console.error('HATA: Bootstrap yüklenmedi!');
        return;
    }
    console.log('✓ Bootstrap yüklendi, versiyon:', bootstrap.Dropdown.VERSION);
    
    // Bildirim sistemini başlat
    window.notificationSystem = new NotificationSystem();
    window.notificationSystem.requestNotificationPermission();
    
    // Dropdown'ı manuel olarak başlat
    const notificationButton = document.getElementById('notificationButton');
    const notificationDropdown = document.getElementById('notificationDropdownMenu');
    
    if (notificationButton && notificationDropdown) {
        console.log('✓ Bildirim butonu ve dropdown bulundu');
        
        // Bootstrap Dropdown instance oluştur
        try {
            // Önce mevcut instance'ı kontrol et
            let dropdownInstance = bootstrap.Dropdown.getInstance(notificationButton);
            
            if (!dropdownInstance) {
                // Yeni instance oluştur
                dropdownInstance = new bootstrap.Dropdown(notificationButton, {
                    autoClose: 'outside',
                    boundary: 'viewport'
                });
                console.log('✓ Dropdown instance oluşturuldu');
            } else {
                console.log('✓ Dropdown instance zaten mevcut');
            }
            
            // Test için butona tıklandığında log
            notificationButton.addEventListener('click', function(e) {
                console.log('Bildirim butonuna tıklandı');
                console.log('Dropdown instance:', dropdownInstance);
                console.log('Button aria-expanded:', notificationButton.getAttribute('aria-expanded'));
            });
            
            // Dropdown açıldığında
            notificationButton.addEventListener('shown.bs.dropdown', function() {
                console.log('✓ Dropdown açıldı!');
                window.notificationSystem.loadNotifications();
            });
            
            // Dropdown kapandığında
            notificationButton.addEventListener('hidden.bs.dropdown', function() {
                console.log('✓ Dropdown kapandı');
            });
        } catch (error) {
            console.error('Dropdown oluşturma hatası:', error);
        }
    } else {
        console.error('HATA: Bildirim butonu veya dropdown bulunamadı!');
        console.log('notificationButton:', notificationButton);
        console.log('notificationDropdown:', notificationDropdown);
    }
    
    // Kullanıcı menüsü dropdown'ını başlat
    const userMenuButton = document.getElementById('userMenuButton');
    const userMenuDropdown = document.getElementById('userMenuDropdown');
    
    if (userMenuButton && userMenuDropdown) {
        console.log('✓ Kullanıcı menüsü butonu ve dropdown bulundu');
        
        try {
            // Önce mevcut instance'ı kontrol et
            let userDropdownInstance = bootstrap.Dropdown.getInstance(userMenuButton);
            
            if (!userDropdownInstance) {
                // Yeni instance oluştur
                userDropdownInstance = new bootstrap.Dropdown(userMenuButton, {
                    autoClose: true,
                    boundary: 'viewport'
                });
                console.log('✓ Kullanıcı menüsü dropdown instance oluşturuldu');
            } else {
                console.log('✓ Kullanıcı menüsü dropdown instance zaten mevcut');
            }
            
            // Test için butona tıklandığında log
            userMenuButton.addEventListener('click', function(e) {
                console.log('Kullanıcı menüsü butonuna tıklandı');
                console.log('Dropdown instance:', userDropdownInstance);
                console.log('Button aria-expanded:', userMenuButton.getAttribute('aria-expanded'));
            });
            
            // Dropdown açıldığında
            userMenuButton.addEventListener('shown.bs.dropdown', function() {
                console.log('✓ Kullanıcı menüsü açıldı!');
            });
            
            // Dropdown kapandığında
            userMenuButton.addEventListener('hidden.bs.dropdown', function() {
                console.log('✓ Kullanıcı menüsü kapandı');
            });
        } catch (error) {
            console.error('Kullanıcı menüsü dropdown oluşturma hatası:', error);
        }
    } else {
        console.log('Kullanıcı menüsü bulunamadı (kullanıcı giriş yapmamış olabilir)');
    }
    
    console.log('=== Bildirim Sistemi Hazır ===');
});
```

**Değişiklikler:**
- Hem `notificationButton` hem de `notificationDropdown` kontrolü eklendi
- Dropdown instance oluşturulurken `autoClose: 'outside'` ve `boundary: 'viewport'` parametreleri eklendi
- Mevcut instance kontrolü eklendi (çift instance oluşmasını önlemek için)
- `hidden.bs.dropdown` event listener'ı eklendi
- Daha detaylı hata mesajları ve console log'ları eklendi

## Test

İki test dosyası oluşturuldu:
1. `test_notification_button.html` - Sadece bildirim butonu testi
2. `test_all_dropdowns.html` - Tüm dropdown'ları test eder (ÖNERİLEN)

`test_all_dropdowns.html` dosyasını tarayıcıda açarak tüm dropdown'ların çalışıp çalışmadığını test edebilirsiniz.

## Kullanım

1. Sayfayı yenileyin
2. **Bildirim simgesine (zil ikonu) tıklayın:**
   - Dropdown menüsü açılmalı
   - "Tümünü Okundu İşaretle" butonuna tıklandığında dropdown kapanmamalı
3. **Kullanıcı menüsüne (erhan Eryılmaz) tıklayın:**
   - Dropdown menüsü açılmalı
   - Menü öğelerine tıklandığında dropdown kapanmalı
4. Console'da log mesajları görünmeli:
   - "✓ Bootstrap yüklendi, versiyon: ..."
   - "✓ Bildirim butonu ve dropdown bulundu"
   - "✓ Dropdown instance oluşturuldu"
   - "✓ Kullanıcı menüsü butonu ve dropdown bulundu"
   - "✓ Kullanıcı menüsü dropdown instance oluşturuldu"
   - "Bildirim butonuna tıklandı" (tıkladığınızda)
   - "✓ Dropdown açıldı!" (açıldığında)

## Sorun Giderme

Eğer hala çalışmıyorsa:

1. **Tarayıcı konsolunu açın** (F12)
2. **Console sekmesine gidin**
3. **Hata mesajlarını kontrol edin**
4. **Şu log'ları arayın:**
   - "Bootstrap yüklenmedi!" → Bootstrap CDN bağlantısını kontrol edin
   - "Bildirim butonu veya dropdown bulunamadı!" → HTML elementlerinin ID'lerini kontrol edin
   - "Dropdown oluşturma hatası" → Bootstrap versiyonunu kontrol edin

5. **Bootstrap versiyonunu kontrol edin:**
   ```javascript
   console.log(bootstrap.Dropdown.VERSION);
   ```
   Versiyon 5.3.7 olmalı.

6. **Dropdown instance'ını kontrol edin:**
   ```javascript
   const btn = document.getElementById('notificationButton');
   const instance = bootstrap.Dropdown.getInstance(btn);
   console.log(instance);
   ```

## Notlar

### Bildirim Dropdown
- Dropdown içindeki "Tümünü Okundu İşaretle" butonuna tıklandığında dropdown kapanmaz (`autoClose: 'outside'` sayesinde)
- Dropdown dışına tıklandığında otomatik olarak kapanır
- ESC tuşuna basıldığında kapanır

### Kullanıcı Menüsü Dropdown
- Menü öğelerine (Profil, Ayarlar, Çıkış Yap) tıklandığında dropdown otomatik kapanır (`autoClose: true` sayesinde)
- Dropdown dışına tıklandığında otomatik olarak kapanır
- ESC tuşuna basıldığında kapanır

### Genel
- Her iki dropdown da mobil cihazlarda düzgün çalışır
- Bootstrap 5.3.7 ile uyumludur
- Erişilebilirlik standartlarına uygundur (aria-labelledby)
