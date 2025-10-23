from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from .models import Siparis, UserProfile
from .forms import SiparisForm

def index(request):
    """Dashboard ana sayfası"""
    # Sadece kontrol edilen siparişlerden lastik satış analizi verileri
    kontrol_siparisler = Siparis.objects.filter(durum='kontrol')
    
    # Lastik satış analizi verileri - mevsim ve araç tipi bazında
    tire_sales_data = {
        'yaz': {
            'binek': kontrol_siparisler.filter(mevsim='yaz', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': kontrol_siparisler.filter(mevsim='yaz', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        },
        'kis': {
            'binek': kontrol_siparisler.filter(mevsim='kis', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': kontrol_siparisler.filter(mevsim='kis', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        },
        'dort_mevsim': {
            'binek': kontrol_siparisler.filter(mevsim='dort-mevsim', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': kontrol_siparisler.filter(mevsim='dort-mevsim', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        }
    }
    
    # Lastik marka dağılımı verileri - sadece kontrol edilen siparişler
    brand_distribution = (
        kontrol_siparisler
        .values('marka')
        .annotate(total_adet=Sum('adet'))
        .order_by('-total_adet')
    )
    
    # Chart için veri hazırlama
    brand_labels = []
    brand_data = []
    brand_colors = [
        '#3b82f6', '#ef4444', '#10b981', '#f59e0b', 
        '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'
    ]
    
    for i, brand in enumerate(brand_distribution):
        brand_labels.append(brand['marka'])
        brand_data.append(brand['total_adet'])
    
    brand_chart_data = {
        'labels': brand_labels,
        'data': brand_data,
        'colors': brand_colors[:len(brand_labels)]
    }
    
    # Son eklenen işlemler (kontrol edilen siparişlerden son 5 kayıt)
    son_islemler = kontrol_siparisler.order_by('-olusturma_tarihi')[:5]
    
    # Gerçek istatistikler - tüm siparişlerden
    toplam_siparis = Siparis.objects.count()
    toplam_ciro = Siparis.objects.aggregate(total=Sum('toplam_fiyat'))['total'] or 0
    kontrol_edilen_siparis = kontrol_siparisler.count()
    toplam_adet = Siparis.objects.aggregate(total=Sum('adet'))['total'] or 0
    
    # Aylık ciro verileri (son 12 ay)
    from datetime import datetime, timedelta
    monthly_revenue = []
    monthly_labels = []
    
    for i in range(11, -1, -1):
        start_date = timezone.now() - timedelta(days=30*i)
        end_date = start_date + timedelta(days=30)
        
        monthly_total = Siparis.objects.filter(
            olusturma_tarihi__gte=start_date,
            olusturma_tarihi__lt=end_date
        ).aggregate(total=Sum('toplam_fiyat'))['total'] or 0
        
        monthly_revenue.append(float(monthly_total))
        monthly_labels.append(start_date.strftime('%b'))
    
    # Şehir bazında satış verileri (cari_firma'dan şehir çıkarımı)
    city_sales = (
        Siparis.objects
        .values('cari_firma')
        .annotate(total_sales=Sum('toplam_fiyat'))
        .order_by('-total_sales')[:8]
    )
    
    city_labels = []
    city_data = []
    for city in city_sales:
        # Basit şehir çıkarımı (firma adından)
        firma = city['cari_firma']
        if 'istanbul' in firma.lower():
            city_name = 'İstanbul'
        elif 'ankara' in firma.lower():
            city_name = 'Ankara'
        elif 'izmir' in firma.lower():
            city_name = 'İzmir'
        elif 'bursa' in firma.lower():
            city_name = 'Bursa'
        elif 'antalya' in firma.lower():
            city_name = 'Antalya'
        elif 'adana' in firma.lower():
            city_name = 'Adana'
        elif 'konya' in firma.lower():
            city_name = 'Konya'
        else:
            city_name = 'Diğer'
        
        if city_name not in city_labels:
            city_labels.append(city_name)
            city_data.append(float(city['total_sales']))
        else:
            idx = city_labels.index(city_name)
            city_data[idx] += float(city['total_sales'])
    
    context = {
        'page_title': 'Dashboard',
        'stats': {
            'total_users': toplam_siparis,
            'revenue': toplam_ciro,
            'orders': kontrol_edilen_siparis,
            'avg_response': toplam_adet
        },
        'tire_sales_data': json.dumps(tire_sales_data),
        'brand_chart_data': json.dumps(brand_chart_data),
        'son_islemler': son_islemler,
        'monthly_revenue': json.dumps(monthly_revenue),
        'monthly_labels': json.dumps(monthly_labels),
        'city_sales_data': json.dumps({
            'labels': city_labels,
            'data': city_data
        })
    }
    return render(request, 'dashboard/index.html', context)

def analytics(request):
    """Analytics sayfası"""
    context = {
        'page_title': 'Analytics',
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def users(request):
    """Users sayfası - Rol bazlı yetkilendirme"""
    # Kullanıcının profilini al
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Eğer profil yoksa varsayılan olarak yönetici rolü ver
        user_profile = UserProfile.objects.create(user=request.user, role='yonetici')
    
    # Admin kontrolü
    is_admin = user_profile.is_admin()
    
    # Kullanıcı listesi - sadece admin görebilir
    users_list = []
    if is_admin:
        users_list = User.objects.all().select_related('userprofile')
    
    # Kullanıcı oluşturma
    if request.method == 'POST' and is_admin:
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role', 'yonetici')
        
        if username and password:
            try:
                # Kullanıcı oluştur
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Profil oluştur
                UserProfile.objects.create(user=user, role=role)
                
                messages.success(request, f'Kullanıcı {username} başarıyla oluşturuldu!')
                return redirect('dashboard:users')
            except Exception as e:
                messages.error(request, f'Kullanıcı oluşturulurken hata: {str(e)}')
        else:
            messages.error(request, 'Kullanıcı adı ve şifre gereklidir!')
    
    context = {
        'page_title': 'Users',
        'is_admin': is_admin,
        'users_list': users_list,
        'user_profile': user_profile,
    }
    return render(request, 'dashboard/users.html', context)

def products(request):
    """Products sayfası"""
    context = {
        'page_title': 'Products',
    }
    return render(request, 'dashboard/products.html', context)

def orders(request):
    """Sipariş Envanteri Dashboard (Orders)"""
    # Hızlı arama (cari ile arama)
    query = request.GET.get('q', '').strip()

    siparisler = Siparis.objects.all()
    if query:
        siparisler = siparisler.filter(cari_firma__icontains=query)

    # Metrikler
    toplam_adet = siparisler.aggregate(total=Sum('adet'))['total'] or 0
    stoktaki_adet = siparisler.filter(ambar='stok').aggregate(total=Sum('adet'))['total'] or 0
    satistaki_adet = siparisler.filter(ambar='satis').aggregate(total=Sum('adet'))['total'] or 0
    toplam_ciro = siparisler.aggregate(total=Sum('toplam_fiyat'))['total'] or 0
    yolda_siparisler = siparisler.filter(durum='yolda').count()
    islemde_siparisler = siparisler.filter(durum='islemde').count()

    # Son eklenen işlemler (son 10 kayıt)
    son_islemler = siparisler.order_by('-olusturma_tarihi')[:10]

    # Marka dağılımı (marka bazında adet toplamı ve kayıt sayısı)
    marka_dagilimi = (
        siparisler.values('marka')
        .annotate(
            kayit_sayisi=Count('id'),
            adet_toplam=Sum('adet'),
            tutar_toplam=Sum('toplam_fiyat'),
        )
        .order_by('-adet_toplam')
    )

    context = {
        'page_title': 'Sipariş Envanteri Dashboard',
        'q': query,
        'stats': {
            'toplam_adet': toplam_adet,
            'stoktaki_adet': stoktaki_adet,
            'satistaki_adet': satistaki_adet,
            'toplam_ciro': toplam_ciro,
            'yolda': yolda_siparisler,
            'islemde': islemde_siparisler,
        },
        'son_islemler': son_islemler,
        'marka_dagilimi': marka_dagilimi,
    }
    return render(request, 'dashboard/orders.html', context)

def forms(request):
    """Kontrol Edilen Siparişler Sayfası"""
    # Filtreleme parametreleri
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Sadece kontrol edilen siparişleri getir
    siparisler = Siparis.objects.filter(durum='kontrol')
    
    # Filtreleme uygula
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # İstatistikler hesapla
    toplam_kontrol = siparisler.count()
    toplam_tutar = siparisler.aggregate(total=Sum('toplam_fiyat'))['total'] or 0
    toplam_adet = siparisler.aggregate(total=Sum('adet'))['total'] or 0
    
    # Grup bazında kontrol sayıları
    grup_istatistikleri = siparisler.values('grup').annotate(
        count=Count('id'),
        total_amount=Sum('toplam_fiyat')
    ).order_by('-count')
    
    # Lastik Satış Analizi - Mevsim ve Araç Tipi bazında
    tire_sales_data = {
        'yaz': {
            'binek': siparisler.filter(mevsim='yaz', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': siparisler.filter(mevsim='yaz', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        },
        'kis': {
            'binek': siparisler.filter(mevsim='kis', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': siparisler.filter(mevsim='kis', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        },
        'dort_mevsim': {
            'binek': siparisler.filter(mevsim='dort-mevsim', grup='binek').aggregate(total=Sum('adet'))['total'] or 0,
            'ticari': siparisler.filter(mevsim='dort-mevsim', grup='ticari').aggregate(total=Sum('adet'))['total'] or 0
        }
    }
    
    # Sayfalama
    paginator = Paginator(siparisler, 15)  # Sayfa başına 15 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Kontrol Edilen Siparişler',
        'siparisler': page_obj,
        'filters': {
            'firma': firma,
            'marka': marka,
            'grup': grup,
            'mevsim': mevsim,
            'ambar': ambar,
            'tarih': tarih_filtre,
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
        },
        'stats': {
            'toplam_kontrol': toplam_kontrol,
            'toplam_tutar': toplam_tutar,
            'toplam_adet': toplam_adet,
        },
        'grup_istatistikleri': grup_istatistikleri,
        'tire_sales_data': json.dumps(tire_sales_data),
    }
    return render(request, 'dashboard/forms.html', context)

def elements(request):
    """Sipariş Envanteri Listesi sayfası"""
    # Filtreleme parametreleri
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    durum = request.GET.get('durum', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Siparişleri getir (iptal edilenleri ve kontrol edilenleri hariç tut)
    siparisler = Siparis.objects.exclude(durum__in=['iptal', 'kontrol'])
    
    # Filtreleme uygula
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if durum:
        siparisler = siparisler.filter(durum=durum)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            # Tarih aralığını günün başı ve sonu olarak ayarla
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            # Geçersiz tarih formatı
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # Sayfalama
    paginator = Paginator(siparisler, 10)  # Sayfa başına 10 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'Sipariş Envanteri',
        'siparisler': page_obj,
        'filters': {
            'firma': firma,
            'marka': marka,
            'grup': grup,
            'durum': durum,
            'mevsim': mevsim,
            'ambar': ambar,
            'tarih': tarih_filtre,
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
        }
    }
    return render(request, 'dashboard/elements.html', context)

def elements_buttons(request):
    """Elements buttons sayfası"""
    context = {
        'page_title': 'Elements - Buttons',
    }
    return render(request, 'dashboard/elements-buttons.html', context)

def elements_alerts(request):
    """Elements alerts sayfası"""
    context = {
        'page_title': 'Elements - Alerts',
    }
    return render(request, 'dashboard/elements-alerts.html', context)

def elements_badges(request):
    """Elements badges sayfası"""
    context = {
        'page_title': 'Elements - Badges',
    }
    return render(request, 'dashboard/elements-badges.html', context)

def elements_cards(request):
    """Elements cards sayfası"""
    context = {
        'page_title': 'Elements - Cards',
    }
    return render(request, 'dashboard/elements-cards.html', context)

def elements_modals(request):
    """Elements modals sayfası"""
    context = {
        'page_title': 'Elements - Modals',
    }
    return render(request, 'dashboard/elements-modals.html', context)

def elements_forms(request):
    """Elements forms sayfası"""
    context = {
        'page_title': 'Elements - Forms',
    }
    return render(request, 'dashboard/elements-forms.html', context)

def elements_tables(request):
    """Elements tables sayfası"""
    context = {
        'page_title': 'Elements - Tables',
    }
    return render(request, 'dashboard/elements-tables.html', context)

def yeni_lastik(request):
    """Yeni lastik ekleme sayfası"""
    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            siparis = form.save()
            messages.success(request, f'Sipariş başarıyla kaydedildi! ID: {siparis.id}')
            return redirect('dashboard:elements')
        else:
            messages.error(request, 'Form hataları var. Lütfen kontrol edin.')
    else:
        form = SiparisForm()
    
    context = {
        'page_title': 'Yeni Lastik Ekle',
        'form': form,
    }
    return render(request, 'dashboard/yeni_lastik.html', context)

def siparis_detay(request, siparis_id):
    """Sipariş detay sayfası"""
    siparis = get_object_or_404(Siparis, id=siparis_id)
    context = {
        'page_title': f'Sipariş Detayı - #{siparis.id}',
        'siparis': siparis,
    }
    return render(request, 'dashboard/siparis_detay.html', context)

def siparis_duzenle(request, siparis_id):
    """Sipariş düzenleme sayfası"""
    siparis = get_object_or_404(Siparis, id=siparis_id)
    
    if request.method == 'POST':
        form = SiparisForm(request.POST, instance=siparis)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sipariş #{siparis.id} başarıyla güncellendi!')
            return redirect('dashboard:elements')
        else:
            messages.error(request, 'Form hataları var. Lütfen kontrol edin.')
    else:
        form = SiparisForm(instance=siparis)
    
    context = {
        'page_title': f'Sipariş Düzenle - #{siparis.id}',
        'form': form,
        'siparis': siparis,
    }
    return render(request, 'dashboard/siparis_duzenle.html', context)

def siparis_sil(request, siparis_id):
    """Sipariş silme"""
    siparis = get_object_or_404(Siparis, id=siparis_id)
    
    if request.method == 'POST':
        siparis_id = siparis.id
        siparis.delete()
        messages.success(request, f'Sipariş #{siparis_id} başarıyla silindi!')
        return redirect('dashboard:elements')
    
    context = {
        'page_title': f'Sipariş Sil - #{siparis.id}',
        'siparis': siparis,
    }
    return render(request, 'dashboard/siparis_sil.html', context)

def siparis_whatsapp(request, siparis_id):
    """WhatsApp mesajı gönder"""
    siparis = get_object_or_404(Siparis, id=siparis_id)
    
    # WhatsApp mesajı oluştur
    mesaj = f"""*Lastik Envanteri - {siparis.cari_firma}*

*Ürün:* {siparis.urun}
*Marka:* {siparis.marka}
*Adet:* {siparis.adet}
*Durum:* {siparis.get_durum_display()}
*Güncellenen Son Tarih:* {timezone.localtime(siparis.guncelleme_tarihi).strftime('%d.%m.%Y %H:%M')}"""
    
    # WhatsApp URL'si oluştur (telefon numarası placeholder)
    whatsapp_url = f"https://wa.me/?text={mesaj.replace(' ', '%20').replace('\n', '%0A')}"
    
    return redirect(whatsapp_url)

def reports(request):
    """İptal Edilen Siparişler Raporu"""
    # Filtreleme parametreleri
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Sadece iptal edilen siparişleri getir
    siparisler = Siparis.objects.filter(durum='iptal')
    
    # Filtreleme uygula
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # İstatistikler hesapla
    toplam_iptal = siparisler.count()
    toplam_tutar = siparisler.aggregate(total=Sum('toplam_fiyat'))['total'] or 0
    toplam_adet = siparisler.aggregate(total=Sum('adet'))['total'] or 0
    
    # Grup bazında iptal sayıları
    grup_istatistikleri = siparisler.values('grup').annotate(
        count=Count('id'),
        total_amount=Sum('toplam_fiyat')
    ).order_by('-count')
    
    # Sayfalama
    paginator = Paginator(siparisler, 15)  # Sayfa başına 15 kayıt
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_title': 'İptal Edilen Siparişler Raporu',
        'siparisler': page_obj,
        'filters': {
            'firma': firma,
            'marka': marka,
            'grup': grup,
            'mevsim': mevsim,
            'ambar': ambar,
            'tarih': tarih_filtre,
            'baslangic_tarihi': baslangic_tarihi,
            'bitis_tarihi': bitis_tarihi,
        },
        'stats': {
            'toplam_iptal': toplam_iptal,
            'toplam_tutar': toplam_tutar,
            'toplam_adet': toplam_adet,
        },
        'grup_istatistikleri': grup_istatistikleri,
    }
    return render(request, 'dashboard/reports.html', context)

def messages_view(request):
    """Messages sayfası"""
    context = {
        'page_title': 'Messages',
    }
    return render(request, 'dashboard/messages.html', context)

def calendar(request):
    """Calendar sayfası"""
    # Örnek etkinlik verileri
    events = [
        {
            'id': 1,
            'title': 'Sipariş Toplantısı',
            'start': '2025-01-15T10:00:00',
            'end': '2025-01-15T11:00:00',
            'color': '#3b82f6',
            'description': 'Aylık sipariş değerlendirme toplantısı'
        },
        {
            'id': 2,
            'title': 'Lastik Teslimatı',
            'start': '2025-01-16T14:00:00',
            'end': '2025-01-16T16:00:00',
            'color': '#10b981',
            'description': 'KONLAS firmasına lastik teslimatı'
        },
        {
            'id': 3,
            'title': 'Stok Kontrolü',
            'start': '2025-01-17T09:00:00',
            'end': '2025-01-17T12:00:00',
            'color': '#f59e0b',
            'description': 'Aylık stok sayımı ve kontrolü'
        },
        {
            'id': 4,
            'title': 'Müşteri Ziyareti',
            'start': '2025-01-18T13:00:00',
            'end': '2025-01-18T15:00:00',
            'color': '#8b5cf6',
            'description': 'TOMAY firması müşteri ziyareti'
        },
        {
            'id': 5,
            'title': 'Rapor Hazırlama',
            'start': '2025-01-20T10:00:00',
            'end': '2025-01-20T17:00:00',
            'color': '#ef4444',
            'description': 'Aylık satış raporu hazırlama'
        }
    ]
    
    context = {
        'page_title': 'Calendar',
        'events': json.dumps(events),
    }
    return render(request, 'dashboard/calendar.html', context)

def files(request):
    """Files sayfası"""
    context = {
        'page_title': 'Files',
    }
    return render(request, 'dashboard/files.html', context)

def settings(request):
    """Settings sayfası"""
    context = {
        'page_title': 'Settings',
    }
    return render(request, 'dashboard/settings.html', context)

def security(request):
    """Security sayfası"""
    context = {
        'page_title': 'Security',
    }
    return render(request, 'dashboard/security.html', context)

def help(request):
    """Help sayfası"""
    context = {
        'page_title': 'Help & Support',
    }
    return render(request, 'dashboard/help.html', context)

def export_excel(request):
    """Sipariş Envanterini Excel'e aktar"""
    # Filtreleme parametrelerini al
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    durum = request.GET.get('durum', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Siparişleri filtrele (iptal edilenleri ve kontrol edilenleri hariç tut)
    siparisler = Siparis.objects.exclude(durum__in=['iptal', 'kontrol'])
    
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if durum:
        siparisler = siparisler.filter(durum=durum)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # Excel dosyası oluştur
    wb = Workbook()
    ws = wb.active
    ws.title = "Sipariş Envanteri"
    
    # Başlık satırı
    headers = [
        'CARI (FIRMA)', 'ÜRÜN', 'MARKA', 'GRUP', 'MEVSİM', 'ADET', 
        'BİRİM FİYAT', 'DURUM', 'AMBAR', 'AÇIKLAMA 1', 'TOPLAM FİYAT', 
        'ÖDEME', 'SMS', 'ÖNE ÇIKAR', 'OLUŞTURMA TARİHİ', 'GÜNCELLEME TARİHİ'
    ]
    
    # Başlık stilini ayarla
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Veri satırları
    for row, siparis in enumerate(siparisler, 2):
        ws.cell(row=row, column=1, value=siparis.cari_firma)
        ws.cell(row=row, column=2, value=siparis.urun)
        ws.cell(row=row, column=3, value=siparis.marka)
        ws.cell(row=row, column=4, value=siparis.get_grup_display())
        ws.cell(row=row, column=5, value=siparis.get_mevsim_display())
        ws.cell(row=row, column=6, value=siparis.adet)
        ws.cell(row=row, column=7, value=siparis.birim_fiyat)
        ws.cell(row=row, column=8, value=siparis.get_durum_display())
        ws.cell(row=row, column=9, value=siparis.get_ambar_display())
        ws.cell(row=row, column=10, value=siparis.aciklama)
        ws.cell(row=row, column=11, value=siparis.toplam_fiyat)
        ws.cell(row=row, column=12, value=siparis.get_odeme_display())
        ws.cell(row=row, column=13, value=siparis.get_sms_durum_display())
        ws.cell(row=row, column=14, value="Evet" if siparis.one_cikar else "Hayır")
        ws.cell(row=row, column=15, value=siparis.olusturma_tarihi.strftime('%d.%m.%Y %H:%M'))
        ws.cell(row=row, column=16, value=siparis.guncelleme_tarihi.strftime('%d.%m.%Y %H:%M'))
    
    # Sütun genişliklerini ayarla
    column_widths = [20, 25, 15, 12, 12, 8, 12, 15, 10, 30, 12, 12, 10, 12, 18, 18]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width
    
    # HTTP response oluştur
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="siparis_envanteri.xlsx"'
    
    # Excel dosyasını response'a yaz
    wb.save(response)
    return response

def export_cancelled_excel(request):
    """İptal Edilen Siparişleri Excel'e aktar"""
    # Filtreleme parametrelerini al
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Sadece iptal edilen siparişleri filtrele
    siparisler = Siparis.objects.filter(durum='iptal')
    
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # Excel dosyası oluştur
    wb = Workbook()
    ws = wb.active
    ws.title = "İptal Edilen Siparişler"
    
    # Başlık satırı
    headers = [
        'ID', 'CARI (FIRMA)', 'ÜRÜN', 'MARKA', 'GRUP', 'MEVSİM', 'ADET', 
        'BİRİM FİYAT', 'AMBAR', 'AÇIKLAMA', 'TOPLAM FİYAT', 
        'ÖDEME', 'SMS', 'ÖNE ÇIKAR', 'OLUŞTURMA TARİHİ', 'İPTAL TARİHİ'
    ]
    
    # Başlık stilini ayarla
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="DC3545", end_color="DC3545", fill_type="solid")  # Kırmızı renk
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Veri satırları
    for row, siparis in enumerate(siparisler, 2):
        ws.cell(row=row, column=1, value=siparis.id)
        ws.cell(row=row, column=2, value=siparis.cari_firma)
        ws.cell(row=row, column=3, value=siparis.urun)
        ws.cell(row=row, column=4, value=siparis.marka)
        ws.cell(row=row, column=5, value=siparis.get_grup_display())
        ws.cell(row=row, column=6, value=siparis.get_mevsim_display())
        ws.cell(row=row, column=7, value=siparis.adet)
        ws.cell(row=row, column=8, value=siparis.birim_fiyat)
        ws.cell(row=row, column=9, value=siparis.get_ambar_display())
        ws.cell(row=row, column=10, value=siparis.aciklama)
        ws.cell(row=row, column=11, value=siparis.toplam_fiyat)
        ws.cell(row=row, column=12, value=siparis.get_odeme_display())
        ws.cell(row=row, column=13, value=siparis.get_sms_durum_display())
        ws.cell(row=row, column=14, value="Evet" if siparis.one_cikar else "Hayır")
        ws.cell(row=row, column=15, value=siparis.olusturma_tarihi.strftime('%d.%m.%Y %H:%M'))
        ws.cell(row=row, column=16, value=siparis.guncelleme_tarihi.strftime('%d.%m.%Y %H:%M'))
    
    # Sütun genişliklerini ayarla
    column_widths = [8, 20, 25, 15, 12, 12, 8, 12, 10, 30, 12, 12, 10, 12, 18, 18]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width
    
    # HTTP response oluştur
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="iptal_edilen_siparisler.xlsx"'
    
    # Excel dosyasını response'a yaz
    wb.save(response)
    return response

def export_checked_excel(request):
    """Kontrol Edilen Siparişleri Excel'e aktar"""
    # Filtreleme parametrelerini al
    firma = request.GET.get('firma', '')
    marka = request.GET.get('marka', '')
    grup = request.GET.get('grup', '')
    mevsim = request.GET.get('mevsim', '')
    ambar = request.GET.get('ambar', '')
    tarih_filtre = request.GET.get('tarih', '')
    baslangic_tarihi = request.GET.get('baslangic_tarihi', '')
    bitis_tarihi = request.GET.get('bitis_tarihi', '')
    
    # Sadece kontrol edilen siparişleri filtrele
    siparisler = Siparis.objects.filter(durum='kontrol')
    
    if firma:
        siparisler = siparisler.filter(cari_firma__icontains=firma)
    if marka:
        siparisler = siparisler.filter(marka__icontains=marka)
    if grup:
        siparisler = siparisler.filter(grup=grup)
    if mevsim:
        siparisler = siparisler.filter(mevsim=mevsim)
    if ambar:
        siparisler = siparisler.filter(ambar=ambar)
    
    # Tarih filtreleme uygula
    now = timezone.now()
    if tarih_filtre:
        if tarih_filtre == 'son-1-ay':
            start_date = now - timedelta(days=30)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-3-ay':
            start_date = now - timedelta(days=90)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'son-6-ay':
            start_date = now - timedelta(days=180)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bugun':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        elif tarih_filtre == 'bu-hafta':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        elif tarih_filtre == 'bu-ay':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
    
    # Özel tarih aralığı filtreleme
    if baslangic_tarihi and bitis_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__range=[start_date, end_date])
        except ValueError:
            pass
    elif baslangic_tarihi:
        try:
            start_date = datetime.strptime(baslangic_tarihi, '%Y-%m-%d')
            start_date = timezone.make_aware(start_date.replace(hour=0, minute=0, second=0))
            siparisler = siparisler.filter(olusturma_tarihi__gte=start_date)
        except ValueError:
            pass
    elif bitis_tarihi:
        try:
            end_date = datetime.strptime(bitis_tarihi, '%Y-%m-%d')
            end_date = timezone.make_aware(end_date.replace(hour=23, minute=59, second=59))
            siparisler = siparisler.filter(olusturma_tarihi__lte=end_date)
        except ValueError:
            pass
    
    # Excel dosyası oluştur
    wb = Workbook()
    ws = wb.active
    ws.title = "Kontrol Edilen Siparişler"
    
    # Başlık satırı
    headers = [
        'CARI (FIRMA)', 'ÜRÜN', 'MARKA', 'GRUP', 'MEVSİM', 'ADET', 
        'BİRİM FİYAT', 'AMBAR', 'AÇIKLAMA', 'TOPLAM FİYAT', 
        'ÖDEME', 'SMS', 'ÖNE ÇIKAR', 'OLUŞTURMA TARİHİ', 'KONTROL TARİHİ'
    ]
    
    # Başlık stilini ayarla
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="FFC107", end_color="FFC107", fill_type="solid")  # Sarı renk
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Veri satırları
    for row, siparis in enumerate(siparisler, 2):
        ws.cell(row=row, column=1, value=siparis.cari_firma)
        ws.cell(row=row, column=2, value=siparis.urun)
        ws.cell(row=row, column=3, value=siparis.marka)
        ws.cell(row=row, column=4, value=siparis.get_grup_display())
        ws.cell(row=row, column=5, value=siparis.get_mevsim_display())
        ws.cell(row=row, column=6, value=siparis.adet)
        ws.cell(row=row, column=7, value=siparis.birim_fiyat)
        ws.cell(row=row, column=8, value=siparis.get_ambar_display())
        ws.cell(row=row, column=9, value=siparis.aciklama)
        ws.cell(row=row, column=10, value=siparis.toplam_fiyat)
        ws.cell(row=row, column=11, value=siparis.get_odeme_display())
        ws.cell(row=row, column=12, value=siparis.get_sms_durum_display())
        ws.cell(row=row, column=13, value="Evet" if siparis.one_cikar else "Hayır")
        ws.cell(row=row, column=14, value=siparis.olusturma_tarihi.strftime('%d.%m.%Y %H:%M'))
        ws.cell(row=row, column=15, value=siparis.guncelleme_tarihi.strftime('%d.%m.%Y %H:%M'))
    
    # Sütun genişliklerini ayarla
    column_widths = [20, 25, 15, 12, 12, 8, 12, 10, 30, 12, 12, 10, 12, 18, 18]
    for col, width in enumerate(column_widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width
    
    # HTTP response oluştur
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="kontrol_edilen_siparisler.xlsx"'
    
    # Excel dosyasını response'a yaz
    wb.save(response)
    return response

def login_view(request):
    """Kullanıcı giriş sayfası"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Hoş geldiniz, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'dashboard:index')
                return redirect(next_url)
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun!')
    
    context = {
        'page_title': 'Giriş Yap',
    }
    return render(request, 'dashboard/login.html', context)

def logout_view(request):
    """Kullanıcı çıkış"""
    if request.user.is_authenticated:
        username = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'Güle güle, {username}!')
    return redirect('dashboard:login')