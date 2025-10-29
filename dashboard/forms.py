from django import forms
from .models import Transaction, TransactionCategory


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'hareket_tipi', 'tarih', 'kasa_adi', 'nakit', 'kredi_karti', 'cari', 'mehmet_havale',
            'aciklama', 'kategori1'
        ]
        widgets = {
            'tarih': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hareket_tipi': forms.Select(attrs={'class': 'form-select'}),
            'kasa_adi': forms.Select(attrs={'class': 'form-select'}),
            'nakit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'kredi_karti': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'cari': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'mehmet_havale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'aciklama': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori1': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Kategori1'i opsiyonel yap
        self.fields['kategori1'].required = False
        # Açıklama alanını opsiyonel yap
        self.fields['aciklama'].required = False

    def clean(self):
        cleaned = super().clean()
        nakit = cleaned.get('nakit') or 0
        kredi = cleaned.get('kredi_karti') or 0
        cari = cleaned.get('cari') or 0
        mehmet = cleaned.get('mehmet_havale') or 0
        
        # En az bir ödeme alanı dolu olmalı
        if nakit + kredi + cari + mehmet <= 0:
            raise forms.ValidationError('En az bir ödeme alanı (Nakit, Kredi Kartı, Cari veya Mehmet Havale) doldurulmalıdır.')
        
        # Sadece bir ödeme türü seçilmeli
        filled_fields = []
        if nakit > 0:
            filled_fields.append('Nakit')
        if kredi > 0:
            filled_fields.append('Kredi Kartı')
        if cari > 0:
            filled_fields.append('Cari')
        if mehmet > 0:
            filled_fields.append('Mehmet Havale')
            
        if len(filled_fields) > 1:
            raise forms.ValidationError(f'Sadece bir ödeme türü seçilmelidir. Şu anda seçili: {", ".join(filled_fields)}')
        
        return cleaned
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
