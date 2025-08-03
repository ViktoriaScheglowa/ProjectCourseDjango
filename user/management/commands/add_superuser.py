from django.core.management import BaseCommand

import user
from user.models import User


class Command(BaseCommand):
    help = "Добавление суперюзера"

    def handle(self, *args, **options):
        super_user: User = User.objects.create(email='admin@admin.com',
                                               first_name='Admin',
                                               last_name='Adminexin',
                                               is_staff=True,
                                               is_active=True,
                                               is_superuser=True)
        super_user.set_password('1234qwer')
        super_user.save()
        self.stdout.write(
            self.style.SUCCESS(f'Успешно создан пользователь-администратор'))
