from django.contrib import admin
from .models import Siparis

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