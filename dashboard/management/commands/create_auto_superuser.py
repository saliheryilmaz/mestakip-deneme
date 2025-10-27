"""
Auto-create superuser if none exists
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Automatically create superuser if none exists'

    def handle(self, *args, **options):
        # Railway environment'de çalış
        if os.environ.get('RAILWAY_ENVIRONMENT'):
            # Eğer hiç kullanıcı yoksa, otomatik oluştur
            if User.objects.filter(is_superuser=True).count() == 0:
                username = os.environ.get('ADMIN_USERNAME', 'admin')
                email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
                password = os.environ.get('ADMIN_PASSWORD', 'admin12345')
                
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username,
                        email=email,
                        password=password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Superuser "{username}" otomatik oluşturuldu!'
                        )
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            f'🔑 Password: {password}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Superuser "{username}" zaten var'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        '✅ Superuser zaten mevcut'
                    )
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'ℹ️  Local environment - skipping auto superuser'
                )
            )

