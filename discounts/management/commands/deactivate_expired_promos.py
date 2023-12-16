from django.core.management.base import BaseCommand
from django.utils import timezone
from discounts.models import PromoCode

class Command(BaseCommand):
    help = 'Делает все истекшие промокоды is_active = False'

    def handle(self, *args, **options):
        expired_promo_codes = PromoCode.objects.filter(expiration_date__lt=timezone.now())
        expired_promo_codes.update(is_active=False)

        self.stdout.write(self.style.SUCCESS('Успешно деактивированы истекшие промокоды'))