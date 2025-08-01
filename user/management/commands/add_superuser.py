from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = "Добавление суперюзера"

    def handle(self, *args, **options):
        super_user: User = User.objects.create(email='admin@admin.com',
                                               is_staff=True,
                                               is_active=True,
                                               is_superuser=True)
        super_user.set_password('123qwe')
        super_user.save()