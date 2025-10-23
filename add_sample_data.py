from dashboard.models import Siparis

# Örnek siparişler oluştur
siparisler = [
    {
        'cari_firma': 'HANLAR YILMAZ',
        'marka': 'MATADOR',
        'urun': '235/65R16 NORDDICA',
        'grup': 'ticari',
        'mevsim': 'kis',
        'adet': 15,
        'birim_fiyat': 5750.00,
        'ambar': 'Stok',
        'odeme': 'havale',
        'sms_durum': 'gonderildi'
    },
    {
        'cari_firma': 'AKIN LASTİK',
        'marka': 'CONTINENTAL',
        'urun': '205/55R16 CONTINENTAL',
        'grup': 'binek',
        'mevsim': 'yaz',
        'adet': 8,
        'birim_fiyat': 3200.00,
        'ambar': 'Satış',
        'odeme': 'nakit',
        'sms_durum': 'gonderildi'
    },
    {
        'cari_firma': 'DEMİR LASTİK',
        'marka': 'MICHELIN',
        'urun': '185/70R14 MICHELIN',
        'grup': 'binek',
        'mevsim': 'dort-mevsim',
        'adet': 12,
        'birim_fiyat': 2800.00,
        'ambar': 'Depo',
        'odeme': 'kredi-karti',
        'sms_durum': 'beklemede'
    },
    {
        'cari_firma': 'AKÜ MERKEZİ',
        'marka': 'VARTA',
        'urun': '12V 70Ah VARTA',
        'grup': 'aku',
        'mevsim': 'dort-mevsim',
        'adet': 6,
        'birim_fiyat': 2500.00,
        'ambar': 'Satış',
        'odeme': 'nakit',
        'sms_durum': 'gonderildi',
        'aciklama': 'Garantili'
    },
    {
        'cari_firma': 'JANT SERVİSİ',
        'marka': 'BBS',
        'urun': '17" ALÜMİNYUM JANT',
        'grup': 'jant',
        'mevsim': 'dort-mevsim',
        'adet': 4,
        'birim_fiyat': 3800.00,
        'ambar': 'Stok',
        'odeme': 'havale',
        'sms_durum': 'gonderildi',
        'aciklama': 'Özel tasarım'
    }
]

# Siparişleri veritabanına ekle
for siparis_data in siparisler:
    Siparis.objects.create(**siparis_data)

print(f'{len(siparisler)} örnek sipariş başarıyla eklendi!')

