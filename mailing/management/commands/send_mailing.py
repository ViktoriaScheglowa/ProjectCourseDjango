from django.core.management import BaseCommand
from django.utils import timezone

from mailing.models import Mailing
from mailing.services import send_message


class Command(BaseCommand):
    help = 'Send current mailing'

    def handle(self, *args, **options):
        now = timezone.now()
        try:
            mailings = Mailing.objects.filter(
                start_sending__lte=now,
                end_sending__gte=now,
                status__in=[Mailing.CREATED, Mailing.ACTIVATED]
            )
            for mailing in mailings:
                send_message(mailing.pk)

                if mailing.status == Mailing.CREATED:
                    mailing.status = Mailing.ACTIVATED
                    mailing.save()
            return 'Рассылки отправлены.'
        except Exception as ex:
            return str(ex)
