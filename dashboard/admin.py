from django.contrib import admin
from .models import Siparis, Event, UserProfile

@admin.register(Siparis)
class SiparisAdmin(admin.ModelAdmin):
    """Sipariş admin paneli"""
    
    list_display = [
        'id', 'cari_firma', 'marka', 'urun', 'grup', 
        'mevsim', 'adet', 'birim_fiyat', 'toplam_fiyat', 
        'durum', 'ambar', 'odeme', 'sms_durum', 'one_cikar', 
        'olusturma_tarihi'
    ]
    
    list_filter = [
        'grup', 'mevsim', 'durum', 'odeme', 'sms_durum', 
        'one_cikar', 'olusturma_tarihi'
    ]
    
    search_fields = [
        'cari_firma', 'marka', 'urun', 'ambar', 'aciklama'
    ]
    
    list_editable = [
        'durum', 'ambar', 'sms_durum', 'one_cikar'
    ]
    
    readonly_fields = [
        'toplam_fiyat', 'olusturma_tarihi', 'guncelleme_tarihi'
    ]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('cari_firma', 'marka', 'urun')
        }),
        ('Kategori', {
            'fields': ('grup', 'mevsim')
        }),
        ('Miktar ve Fiyat', {
            'fields': ('adet', 'birim_fiyat', 'toplam_fiyat')
        }),
        ('Durum', {
            'fields': ('durum', 'ambar', 'odeme', 'sms_durum')
        }),
        ('Ek Bilgiler', {
            'fields': ('aciklama', 'one_cikar'),
            'classes': ('collapse',)
        }),
        ('Zaman Damgaları', {
            'fields': ('olusturma_tarihi', 'guncelleme_tarihi'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-olusturma_tarihi']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Etkinlik admin paneli"""
    
    list_display = [
        'id', 'title', 'type', 'date', 'time', 'priority', 
        'location', 'created_by', 'created_at'
    ]
    
    list_filter = [
        'type', 'priority', 'date', 'recurring', 'created_at'
    ]
    
    search_fields = [
        'title', 'description', 'location', 'attendees'
    ]
    
    list_editable = [
        'type', 'priority'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'description', 'type', 'priority')
        }),
        ('Tarih ve Zaman', {
            'fields': ('date', 'time', 'duration')
        }),
        ('Konum ve Katılımcılar', {
            'fields': ('location', 'attendees')
        }),
        ('Tekrarlama', {
            'fields': ('recurring', 'recurrence'),
            'classes': ('collapse',)
        }),
        ('Hatırlatıcılar', {
            'fields': ('reminders',),
            'classes': ('collapse',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yeni kayıt ise
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Kullanıcı Profili admin paneli"""
    
    list_display = [
        'user', 'role', 'created_at', 'updated_at'
    ]
    
    list_filter = [
        'role', 'created_at'
    ]
    
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'user__email'
    ]
    
    readonly_fields = [
        'created_at', 'updated_at'
    ]