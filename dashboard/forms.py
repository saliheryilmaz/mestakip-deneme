from django import forms
from .models import Siparis

class SiparisForm(forms.ModelForm):
    """Sipariş formu"""
    
    class Meta:
        model = Siparis
        fields = [
            'cari_firma', 'marka', 'urun', 'grup', 'mevsim',
            'adet', 'birim_fiyat', 'toplam_fiyat', 'durum', 'ambar', 
            'odeme', 'sms_durum', 'aciklama', 'one_cikar', 'iptal_sebebi'
        ]
        widgets = {
            'cari_firma': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Müşteri firma adını girin'
            }),
            'marka': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lastik markasını girin'
            }),
            'urun': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lastik model ve özelliklerini girin'
            }),
            'grup': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mevsim': forms.Select(attrs={
                'class': 'form-select'
            }),
            'adet': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'birim_fiyat': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'value': '0'
            }),
            'toplam_fiyat': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'readonly': True
            }),
            'durum': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ambar': forms.Select(attrs={
                'class': 'form-select'
            }),
            'odeme': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sms_durum': forms.Select(attrs={
                'class': 'form-select'
            }),
            'aciklama': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Ek açıklama girin'
            }),
            'one_cikar': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'iptal_sebebi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'İptal sebebini girin',
                'id': 'iptal-sebebi-field'
            })
        }
        labels = {
            'cari_firma': 'CARI (FIRMA)',
            'marka': 'MARKA',
            'urun': 'ÜRÜN (LASTIK MARKA MODEL)',
            'grup': 'GRUP',
            'mevsim': 'MEVSİM',
            'adet': 'ADET',
            'birim_fiyat': 'BİRİM FİYAT',
            'toplam_fiyat': 'TOPLAM FİYAT',
            'durum': 'DURUM',
            'ambar': 'AMBAR',
            'odeme': 'ÖDEME',
            'sms_durum': 'SMS DURUMU',
            'aciklama': 'AÇIKLAMA',
            'one_cikar': 'ÖNE ÇIKAR',
            'iptal_sebebi': 'İPTAL SEBEBİ'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Boş seçenekler ekle
        self.fields['grup'].empty_label = "--------"
        self.fields['mevsim'].empty_label = "--------"
        self.fields['durum'].empty_label = "--------"
        self.fields['ambar'].empty_label = "--------"
        self.fields['odeme'].empty_label = "--------"
        self.fields['sms_durum'].empty_label = "--------"
        
        # Zorunlu alanları işaretle
        self.fields['cari_firma'].required = True
        self.fields['marka'].required = True
        self.fields['urun'].required = True
        self.fields['grup'].required = True
        self.fields['mevsim'].required = True
        self.fields['adet'].required = True
        self.fields['birim_fiyat'].required = True
        self.fields['ambar'].required = True
        self.fields['odeme'].required = True
        
        # Durum iptal ise iptal_sebebi zorunlu
        if self.data.get('durum') == 'iptal':
            self.fields['iptal_sebebi'].required = True
            self.fields['iptal_sebebi'].widget.attrs['required'] = True
    
    def clean(self):
        cleaned_data = super().clean()
        durum = cleaned_data.get('durum')
        iptal_sebebi = cleaned_data.get('iptal_sebebi')
        
        # Durum iptal ise sebep zorunlu
        if durum == 'iptal' and not iptal_sebebi:
            raise forms.ValidationError({
                'iptal_sebebi': 'İptal edilecek siparişler için iptal sebebi belirtmek zorunludur.'
            })
        
        return cleaned_data
