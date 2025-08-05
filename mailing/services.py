from django.utils import timezone
from django.utils.timezone import localtime
from django.core.mail import send_mail

import mailing
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingAttempt


def send_message(pk, request=None):
    """Отправка рассылки по требованию"""
    mailing = Mailing.objects.get(pk=pk)
    now = timezone.now()

    if request and mailing.owner != request.user:
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer=f'Рассылку пытался отправить посторонний человек: {request.user.email}',
            date_attempt=now,
        )
        return False

    subject = mailing.message.subject
    message=mailing.message.text
    client_list = [client.email for client in mailing.client.all()]

    if mailing.status == Mailing.ENDED:
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer='Рассылка уже завершена',
            date_attempt=now,
        )
        return False

    if now < mailing.start_sending:
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer=f'Время рассылки еще не наступило (начало - {mailing.start_sending}, сейчас - {now})',
            date_attempt=now,
        )
        return False
    elif now > mailing.end_sending:
        mailing.status = Mailing.ENDED
        mailing.save()
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer=f'Время рассылки уже прошло (конец - {mailing.end_sending}, сейчас - {now})',
            date_attempt=now,
        )
        return False

    if not client_list:
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer='Нет получателей рассылки',
            date_attempt=now,
        )
        return False

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=client_list,
            fail_silently=False,
        )

        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer='Рассылка отправлена',
            date_attempt=now,
        )
        if mailing.status == Mailing.CREATED:
            mailing.status = Mailing.ACTIVATED
            mailing.save()

        return True

    except Exception as ex:
        MailingAttempt.objects.create(
            mailing=mailing,
            status=MailingAttempt.UNSUCCESS,
            answer=str(ex),
            date_attempt=now,
        )
        return False
