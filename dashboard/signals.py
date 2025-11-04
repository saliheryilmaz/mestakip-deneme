from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import TransactionCategory, UserProfile

@receiver(post_save, sender=User)
def create_user_categories(sender, instance, created, **kwargs):
    """Yeni kullanıcı oluşturulduğunda varsayılan kategorileri oluştur"""
    if created:
        # Varsayılan kategoriler
        default_categories = [
            'Satış',
            'Alış',
            'Personel Giderleri',
            'Kira',
            'Elektrik',
            'Su',
            'Telefon',
            'İnternet',
            'Yakıt',
            'Bakım-Onarım',
            'Vergi',
            'Sigorta',
            'Banka Masrafları',
            'Diğer Gelirler',
            'Diğer Giderler'
        ]
        
        # Her kategoriyi oluştur
        for category_name in default_categories:
            TransactionCategory.objects.create(
                name=category_name,
                created_by=instance,
                parent=None
            )

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Kullanıcı profili oluştur ve rolü Django bayraklarına göre senkronize et"""
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    # Süperuser veya staff ise rolü admin yap, değilse mevcut rolü koru (varsayılan yonetici)
    desired_role = 'admin' if (instance.is_superuser or instance.is_staff) else profile.role or 'yonetici'
    if profile.role != desired_role:
        profile.role = desired_role
        profile.save(update_fields=['role'])