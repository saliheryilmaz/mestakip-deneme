from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Kullanıcı profil modeli - rol yönetimi için"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('yonetici', 'Yönetici'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='yonetici', verbose_name="Rol")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_admin(self):
        """Admin rolü kontrolü"""
        return self.role == 'admin'
    
    def is_yonetici(self):
        """Yönetici rolü kontrolü"""
        return self.role == 'yonetici'

class Siparis(models.Model):
    """Sipariş modeli - Lastik, Akü, Jant siparişleri"""
    
    GRUP_CHOICES = [
        ('ticari', 'Ticari'),
        ('binek', 'Binek'),
        ('aku', 'Akü'),
        ('jant', 'Jant'),
    ]
    
    MEVSIM_CHOICES = [
        ('kis', 'Kış'),
        ('yaz', 'Yaz'),
        ('dort-mevsim', '4 Mevsim'),
    ]
    
    DURUM_CHOICES = [
        ('yolda', 'Yolda'),
        ('islemde', 'İşleme Devam Ediyor'),
        ('teslim', 'Teslim Edildi'),
        ('kontrol', 'Kontrol Edildi'),
        ('iptal', 'İptal Edildi'),
    ]
    
    ODEME_CHOICES = [
        ('kredi-karti', 'Kredi Kartı'),
        ('havale', 'Havale'),
        ('cari-hesap', 'Cari Hesap'),
    ]
    
    SMS_CHOICES = [
        ('gonderilmedi', 'Gönderilmedi'),
        ('gonderildi', 'Gönderildi'),
    ]
    
    AMBAR_CHOICES = [
        ('stok', 'Stok'),
        ('satis', 'Satış'),
    ]
    
    # Temel Bilgiler
    cari_firma = models.CharField(max_length=200, verbose_name="CARI (FIRMA)")
    marka = models.CharField(max_length=100, verbose_name="MARKA")
    urun = models.CharField(max_length=300, verbose_name="ÜRÜN (LASTIK MARKA MODEL)")
    
    # Kategori Bilgileri
    grup = models.CharField(max_length=20, choices=GRUP_CHOICES, verbose_name="GRUP")
    mevsim = models.CharField(max_length=20, choices=MEVSIM_CHOICES, verbose_name="MEVSİM")
    
    # Miktar ve Fiyat
    adet = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        verbose_name="ADET"
    )
    birim_fiyat = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="BİRİM FİYAT"
    )
    toplam_fiyat = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="TOPLAM FİYAT"
    )
    
    # Durum Bilgileri
    durum = models.CharField(max_length=20, choices=DURUM_CHOICES, default='yolda', verbose_name="DURUM")
    ambar = models.CharField(max_length=20, choices=AMBAR_CHOICES, default='stok', verbose_name="AMBAR")
    
    # Ödeme ve İletişim
    odeme = models.CharField(max_length=20, choices=ODEME_CHOICES, verbose_name="ÖDEME")
    sms_durum = models.CharField(max_length=20, choices=SMS_CHOICES, default='gonderilmedi', verbose_name="SMS")
    
    # Ek Bilgiler
    aciklama = models.TextField(blank=True, null=True, verbose_name="AÇIKLAMA")
    one_cikar = models.BooleanField(default=False, verbose_name="ÖNE ÇIKAR")
    
    # Zaman Damgaları
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.cari_firma} - {self.urun} ({self.adet} adet)"
    
    def save(self, *args, **kwargs):
        # Toplam fiyatı otomatik hesapla
        self.toplam_fiyat = self.adet * self.birim_fiyat
        super().save(*args, **kwargs)
    
    def get_grup_display_color(self):
        """Grup için renk döndür"""
        colors = {
            'ticari': 'warning',
            'binek': 'success',
            'aku': 'warning',
            'jant': 'info',
        }
        return colors.get(self.grup, 'secondary')
    
    def get_durum_display_color(self):
        """Durum için renk döndür"""
        colors = {
            'yolda': 'info',
            'islemde': 'primary',
            'teslim': 'success',
            'kontrol': 'warning',
            'iptal': 'danger',
        }
        return colors.get(self.durum, 'secondary')
    
    def get_mevsim_display_color(self):
        """Mevsim için renk döndür"""
        colors = {
            'kis': 'info',
            'yaz': 'warning',
            'dort-mevsim': 'primary',
        }
        return colors.get(self.mevsim, 'secondary')
    
    def get_sms_display_color(self):
        """SMS durumu için renk döndür"""
        colors = {
            'gonderildi': 'success',
            'gonderilmedi': 'danger',
        }
        return colors.get(self.sms_durum, 'secondary')

class Event(models.Model):
    """Takvim etkinlikleri modeli"""
    
    TYPE_CHOICES = [
        ('event', 'Etkinlik'),
        ('meeting', 'Toplantı'),
        ('task', 'Görev'),
        ('reminder', 'Hatırlatıcı'),
        ('deadline', 'Son Tarih'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Düşük'),
        ('medium', 'Orta'),
        ('high', 'Yüksek'),
    ]
    
    RECURRENCE_CHOICES = [
        ('none', 'Tekrarlanmaz'),
        ('daily', 'Günlük'),
        ('weekly', 'Haftalık'),
        ('biweekly', '2 Haftada Bir'),
        ('monthly', 'Aylık'),
        ('yearly', 'Yıllık'),
    ]
    
    # Temel Bilgiler
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='event', verbose_name="Tür")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Öncelik")
    
    # Tarih ve Zaman
    date = models.DateField(verbose_name="Tarih")
    time = models.TimeField(verbose_name="Başlangıç Saati")
    duration = models.PositiveIntegerField(default=60, verbose_name="Süre (dakika)")
    
    # Konum ve Katılımcılar
    location = models.CharField(max_length=300, blank=True, null=True, verbose_name="Konum")
    attendees = models.TextField(blank=True, null=True, verbose_name="Katılımcılar")
    
    # Tekrarlama
    recurring = models.BooleanField(default=False, verbose_name="Tekrarlanan")
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='none', verbose_name="Tekrar Deseni")
    
    # Hatırlatıcılar (JSON formatında)
    reminders = models.TextField(blank=True, null=True, verbose_name="Hatırlatıcılar")
    
    # Oluşturan kullanıcı
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Oluşturan")
    
    # Zaman Damgaları
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"
    
    def get_type_color(self):
        """Etkinlik türü için renk döndür"""
        colors = {
            'event': '#3b82f6',
            'meeting': '#10b981',
            'task': '#f59e0b',
            'reminder': '#8b5cf6',
            'deadline': '#ef4444'
        }
        return colors.get(self.type, '#6b7280')
    
    def get_priority_color(self):
        """Öncelik için renk döndür"""
        colors = {
            'low': '#10b981',
            'medium': '#f59e0b',
            'high': '#ef4444'
        }
        return colors.get(self.priority, '#6b7280')
    
    def get_duration_display(self):
        """Süreyi okunabilir formatta döndür"""
        if self.duration == 480:
            return 'Tüm gün'
        hours = self.duration // 60
        minutes = self.duration % 60
        
        if hours == 0:
            return f'{minutes} dakika'
        elif minutes == 0:
            return f'{hours} saat'
        else:
            return f'{hours}s {minutes}d'